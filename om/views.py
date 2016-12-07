import csv
from datetime import date

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from crm.models import Company
from om.models import *
from om import forms
from indumatic.views import PdfView
from indumatic.pdftools import make_pdf

class CartItemCreateView(CreateView):
    model = CartItem
    success_url = "/"

    @method_decorator(permission_required('om.add_order',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CartItemCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the same offer is already in the cart, simply add the quantities.
        """
        obj = form.save(commit=False)
        try:
            item = CartItem.objects.get(offer=obj.offer)
        except ObjectDoesNotExist:
            form.save(commit=True)
        else:
            item.quantity = item.quantity + obj.quantity
            item.save()
        return HttpResponseRedirect(obj.offer.article.get_absolute_url())

class CartItemDeleteView(DeleteView):
    model = CartItem
    success_url = '/om/cartitem/list/'
    
    @method_decorator(permission_required('om.delete_cartitem',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(CartItemDeleteView, self).dispatch(*args, **kwargs)

class OfferCreateView(CreateView):
    model = Offer
    form_class = forms.OfferForm
    
    @method_decorator(permission_required('om.add_offer',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OfferCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.article.get_absolute_url()

    def form_invalid(self, form):
        ##TODO: improve this to show form errors
        id = self.request.POST['article']
        return HttpResponseRedirect(reverse('wm_article_detail', args=[id]))

class OfferUpdateView(UpdateView):
    model = Offer
    form_class = forms.OfferForm
    
    @method_decorator(permission_required('om.change_offer',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OfferUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.article.get_absolute_url()

class OfferExpireView(View):
    @method_decorator(permission_required('om.change_offer',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OfferExpireView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        offer = get_object_or_404(Offer, id=self.kwargs['pk'])
        if not offer.expired_on:
            offer.expired_on = date.today()
            offer.save()
            messages.success(request, _("Offer has expired."))
        return HttpResponseRedirect(offer.article.get_absolute_url())

class OrderCreateView(CreateView):
    form_class = forms.OrderForm
    template_name = "om/order_form.html"
    
    @method_decorator(permission_required('om.add_order',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OrderCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        return {'company': self.kwargs['pk']}

    def get_context_data(self, **kwargs):
        ctx = super(OrderCreateView, self).get_context_data(**kwargs)
        supplier = get_object_or_404(Company, id=self.kwargs['pk'])
        items = CartItem.objects.filter(offer__company=supplier).extra(
            select={"cost": "om_offer.invoice_price*om_cartitem.quantity"}
        )
        ctx.update({
            'supplier': supplier,
            'items': items,
        })
        return ctx

    def form_valid(self, form):
        pwd = form.cleaned_data.get('password', None)
        if not self.request.user.check_password(pwd):
            return HttpResponseRedirect(reverse('logout_then_login'))
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        for item in form.cleaned_data["items"]:
            OrderItem.objects.create(
                order=obj,
                ordered_quantity=item.quantity,
                offer=item.offer
            )
            item.delete()
        return HttpResponseRedirect(obj.get_absolute_url())

class OrderDetailView(DetailView):
    model = Order
    context_object_name = 'order'

    def get_subject_template(self):
        return get_template('om/order_subject.txt')

    def get_body_template(self):
        return get_template('om/order_body.txt')

    def post(self, request, *args, **kwargs):
        """Send an email with the order report to the supplier."""
        self.object = self.get_object()
        ctx = self.get_context_data(**kwargs)
        ctx.update({'pagesize': 'A4'})
        items = OrderItem.objects.filter(order=self.object).extra(
            select={"cost": "select (om_offer.invoice_price*om_orderitem.ordered_quantity) from om_offer where om_offer.id=om_orderitem.offer_id"}
        )
        ctx.update({'items': items})
        html = render_to_string(
            'om/order_pdf.html',
            ctx,
            context_instance=RequestContext(request)
        )
        try:
            document = make_pdf(html)
        except Exception as e:
            if settings.DEBUG:
                return HttpResponse(e.strerror)
            else:
                messages.error(
                    self.request,
                    _("The pdf report for the order could not be made.")
                )
        else:
            subject = self.get_subject_template().render(Context(ctx))
            body = self.get_body_template().render(Context(ctx))
            message = EmailMessage(
                subject=subject.rstrip(),
                body=body,
                from_email='erp@indumatic.net',
                to=self.object.recipient_list,
                cc=['oficina.tecnica@indumatic.net',],
                attachments=[
                    ('%s.pdf' % self.object,
                        document.getvalue(),
                        'application/pdf'),
                ],
                headers={'Reply-To': 'oficina.tecnica@indumatic.net'}
            )
            try:
                message.send()
            except Exception as e:
                messages.error(self.request, e)
            else:
                messages.success(self.request, _("The order was successfully sent."))
        return HttpResponseRedirect(reverse('om_order_pending'))

class OrderByCompanyListView(ListView):
    context_object_name = "item_list"
    paginate_by = 10
    template_name = 'om/orderitem_by_company.html'

    def get_queryset(self):
        return OrderItem.objects.filter(offer__company__id=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        ctx = super(OrderByCompanyListView, self).get_context_data(*args, **kwargs)
        company = get_object_or_404(Company, id=self.kwargs['pk'])
        ctx.update({
            'company': company,
        })
        return ctx

class OrderReceiveView(TemplateView):
    template_name = "om/order_receive.html"
    
    @method_decorator(permission_required('om.change_order',
        raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(OrderReceiveView, self).dispatch(*args, **kwargs)

    def get_formset_class(self):    
        return modelformset_factory(
            OrderItem,
            form=forms.OrderItemReceptionForm,
            extra=0
        )

    def get_context_data(self, *args, **kwargs):
        ctx = super(OrderReceiveView, self).get_context_data(*args, **kwargs)
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        items = order.orderitem_set.extra(
            select={ 'pending': 'ordered_quantity - received_quantity' }
        )
        OrderItemFormSet = self.get_formset_class()
        formset = OrderItemFormSet(queryset=items)
        ctx.update({
            'order': order,
            'formset': formset,
        })
        return ctx

    def post(self, request, *args, **kwargs):
        inventory = getattr(settings, "INVENTORY_IN_PROGRESS", False)
        if inventory:
            raise PermissionDenied
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        OrderItemFormSet = self.get_formset_class()
        formset = OrderItemFormSet(self.request.POST)
        #completed = True
        for form in formset:
            if form.is_valid():
                receive = form.cleaned_data['receive']
                retail_price = form.cleaned_data['retail_price']
                invoice_price = form.cleaned_data['invoice_price']
                item = form.save(commit=False)
                if retail_price is not None:
                    item.offer.retail_price = retail_price
                if invoice_price is not None:
                    item.offer.invoice_price = invoice_price
                if retail_price is not None or invoice_price is not None:
                    item.offer.created_on = date.today()
                    item.offer.save()
                if receive is not None:
                    item.received_quantity += receive
                    if item.received_quantity >= item.ordered_quantity:
                        item.completed_on = date.today()
                    #else:
                    #   completed = False
                    ## update the article stock
                        item.offer.article.update_stock(receive)
                #else:
                #   completed = False
                item.save()
        ## mark the order as completed
        #if completed:
        try:
            order.orderitem_set.get(completed_on__isnull=True)
        except ObjectDoesNotExist:
            order.completed_on = date.today()
            order.save()
        except:
            pass
        return HttpResponseRedirect(
            reverse('om_order_receive', args=[self.kwargs['pk']])
        )

class OrderPdfView(PdfView):
    template_name = 'om/order_pdf.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(OrderPdfView, self).get_context_data(*args, **kwargs)
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        items = OrderItem.objects.filter(order=order).extra(
            select={"cost": "select (om_offer.invoice_price*om_orderitem.ordered_quantity) from om_offer where om_offer.id=om_orderitem.offer_id"}
        )
        ctx.update({
            'order': order,
            'items': items,
        })
        return ctx

class OrderCsvView(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['pk'])
        csvtemplate = get_object_or_404(CsvTemplate, company=order.company)
        response = HttpResponse(content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename="%s.txt"' % order.id
        writer = csv.writer(response)
        for line in order.orderitem_set.all():
            writer.writerow(line.as_csv(csvtemplate.template))

        return response

class OrderItemPendingView(ListView):
    model = OrderItem
    context_object_name = "item_list"
    paginate_by = 10
    template_name = 'om/orderitem_pending_list.html'
    
    def get_queryset(self):
        qs = OrderItem.objects.filter(completed_on__isnull=True)
        if 'pk' in self.kwargs.keys():
            qs = qs.filter(offer__company__id=self.kwargs['pk'])
        return qs
