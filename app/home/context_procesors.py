
import logging
from .models import SiteNav


logger = logging.getLogger(__name__)
def sidebarNav(request):
    ret =  {
        "sidebarNav":SiteNav.objects.order_by("displayOrder").all()
    }
    
    
    return ret
    
