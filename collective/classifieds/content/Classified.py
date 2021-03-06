__author__ = """Four Digits <Ralph Jacobs>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFPlone import utils
from Acquisition import aq_inner, aq_parent
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from collective.classifieds.config import *
from collective.classifieds import _

schema = Schema((
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/html',),
        widget=RichWidget(
            label=_(
                u'classifieds_classified_description',
                default=u'Description',
            ),
            description=_(
                u'classifieds_classified_description_description',
                default=u'Description of the classified',
            ),
        ),
        default_output_type='text/html',
        searchable=True,
        required=True,
    ),
    ImageField(
        name='image',
        widget=ImageField._properties['widget'](
            label=_(
                u'classifieds_classified_image',
                default=u'Image',
            ),
            description=_(
                u'classifieds_classified_image_description',
                default=u'Image of the classified',
            ),
        ),
        storage=AttributeStorage(),
        max_size=(768, 768),
        sizes={'large': (768, 768),
                   'preview': (400, 400),
                   'mini': (200, 200),
                   'thumb': (128, 128),
                   'tile':  (64, 64),
                   'icon':  (32, 32),
                   'listing': (16, 16),
                  },
    ),
    ImageField(
        name='additionalimage',
        widget=ImageField._properties['widget'](
            label=_(
                u'classifieds_classified_additionalimage',
                default=u'Additional image',
            ),
            description=_(
                u'classifieds_classified_additionalimage_desc',
                default=u'Additional image of the classified',
            ),
        ),
        storage=AttributeStorage(),
        max_size=(768, 768),
        sizes={'large': (768, 768),
                   'preview': (400, 400),
                   'mini': (200, 200),
                   'thumb': (128, 128),
                   'tile': (64, 64),
                   'icon': (32, 32),
                   'listing': (16, 16),
                  },
    ),
    FloatField(
        name='price',
        widget=DecimalWidget(
            label=_(
                u'classifieds_classified_price',
                default=u'Price',
            ),
            description=_(
                u'classifieds_classified_price_description',
                default=u'Price of the classified',
            ),
        ),
        validators=('isFloat',),
        required=False,
        searchable=True,
    ),
    StringField(
        name='externalurl',
        widget=StringWidget(
            label=_(
                u'classifieds_classified_externalurl',
                default=u'External URL',
            ),
            description=_(
                u'classifieds_classified_externalurl_description',
                default=u'External URL to find more information about the classified',
            ),
        ),
        validators=('isURL',),
        required=False,
        searchable=False,
    ),
),
)

Classified_schema = BaseSchema.copy() + \
    schema.copy()


class Classified(BaseContent, BrowserDefaultMixin):
    """
        Represents a Classified
    """
    security = ClassSecurityInfo()
    implements(interfaces.IClassified)

    meta_type = 'Classified'
    _at_rename_after_creation = True

    schema = Classified_schema

    def getPath(self):
        """Gets the path of the object"""
        path = '/'.join(self.getPhysicalPath())
        return path

    def hasImage(self):
        """checks if the classified has a image"""
        if self.getImage():
            return True
        return False

    def getImageTile(self, **kwargs):
        """Get image tile url, relative to plone site."""
        if self.hasImage():
            imgtileurl = self.getImage().absolute_url(1) + '_tile'
            portal_obj = getToolByName(self, 'portal_url').getPortalObject()
            portal_url = portal_obj.absolute_url(1)
            imgtileurl = imgtileurl.replace(portal_url, '')
            return imgtileurl
        return ''

    def getClassifiedsCategory(self):
        """Get classifieds category"""
        return "%s" % (self.getParentNode().Title())

    def getClassifiedsCategoryPath(self):
        """Get classifieds category path"""
        return "%s" % (self.getParentNode().getPath())

    def check_delete_permission(self):
        """Check if user may delete object"""
        if getSecurityManager().checkPermission("Delete objects", self):
            username = getSecurityManager().getUser().getUserName()
            if username == self.getOwner().getId():
                return True
        return False

    def delete(self):
        """Delete this object"""
        parent = self.aq_inner.aq_parent
        if self.check_delete_permission():
            parent._delObject(self.id)
            return self.REQUEST.RESPONSE.redirect("%s?classified_title=%s&portal_status_message=%s" % (parent.absolute_url(), self.Title(), "has been deleted."))
        return self.REQUEST.RESPONSE.redirect("%s?classified_title=%s&portal_status_message=%s %s" % (parent.absolute_url(), self.Title(), "has not been deleted."))

registerType(Classified, PROJECTNAME)
# end of class Classified
