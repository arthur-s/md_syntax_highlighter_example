from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
from gallery.models import GalleryContent

# from markdown2 import markdown
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class SiteNewsItem(models.Model):
    # TODO: Define fields here
    text = models.TextField(
        max_length=512,
        verbose_name=_('Text'),
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date'),
    )

    class Meta:
        verbose_name = "NewsItem"
        verbose_name_plural = "NewsItems"

    # def __str__(self):
    #     pass

    
# This class is for syntax highlight
class MyRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


class MarkdownPageContent(models.Model):
    content = models.TextField()

    class Meta:
        abstract = True

    def render(self, **kwargs):
        # return markdown(self.content.strip(), extras=['code-friendly', 'fenced-code-blocks', ])
        renderer = MyRenderer()
        md = mistune.Markdown(renderer=renderer)
        # now we can convert text to md, wrapped in <article> tag
        return '<article class="markdown-body">' +  md.render(self.content.strip()) + '</article>'

Page.register_extensions(
    'feincms.module.extensions.datepublisher',
    'feincms.module.extensions.translations',
    'feincms.module.extensions.ct_tracker',
    'feincms.module.extensions.featured',
    'feincms.module.page.extensions.navigation',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.titles'
    )

Page.register_templates({
    'title': _('Standard template'),
    'path': 'pages/template1.html',
    'regions': (
        ('main', _('Main content area')),
        ('sidebar', _('Sidebar'), 'inherited'),
        ),
    })

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
    ))
Page.create_content_type(GalleryContent)

Page.create_content_type(MarkdownPageContent)
