# -*- coding: utf-8 -*-
# Odoo, Open Source Personalized All in One Reports.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api, tools
from odoo.exceptions import AccessError
from odoo.sql_db import TestCursor
from odoo.tools import config
from odoo.tools.misc import find_in_path
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
from base64 import b64decode
from logging import getLogger
from PIL import Image
import io
from io import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.utils import PdfReadError


try:
    from PyPDF2 import PdfFileWriter, PdfFileReader  # pylint: disable=W0404
    from PyPDF2.utils import PdfReadError  # pylint: disable=W0404
except ImportError:
    pass
try:
    # we need this to be sure PIL has loaded PDF support
    from PIL import PdfImagePlugin  # noqa: F401
except ImportError:
    pass
logger = getLogger(__name__)



Selection_Field = [
            ('classic', 'Classic Report'),
            ('fency', 'Fency Report'),
            ('vintage', 'Vintage Report'),
            ('retro', 'Retro Report'),
            ('modern', 'Modern Report'),
            ('canva', 'Canva Report'),
            ('professional', 'Professional Report'),
            ('western', 'Western Report'),
            ('elegant', 'Elegant Report'),
            ('shine', 'Shine Report'),
            ('odoo_standard', 'Odoo Default'),
        ]


class ResCompany(models.Model):
    _inherit = "res.company"

    temp_selection = fields.Selection(Selection_Field, 'Select Template For Sale,Purchase,Stock & Account')
    add_watermark = fields.Boolean('Want Watermark?')
    add_signature = fields.Boolean('Want Signature?')
    watermark_selection = fields.Selection([('letter_head', 'Letter Head'), ('company_logo', 'Company Logo'), ('custom_name', 'Text')], 'Watermark Selection')
    custom_watermark_name = fields.Char('Watermark Name')
    add_product_image = fields.Boolean('Show Product Image in Report')
    sale_header_footer = fields.Char('Select Header & Footer Color')
    primary_color = fields.Char('Select Primary Color')
    secondary_color = fields.Char('Select Secondary Color')
    sale_font_color = fields.Char('Select Font Color')
    letter_head = fields.Binary(string='Letter Logo')
    signature_logo = fields.Binary(string='Signature Logo')






class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'


    @api.multi
    def _post_pdf(self, save_in_attachment, pdf_content=None, res_ids=None):
        user = self.env['res.users'].browse(self.env.uid)
        result = super(IrActionsReport, self)._post_pdf(save_in_attachment, pdf_content=pdf_content, res_ids=res_ids)
        if user.company_id.temp_selection == 'odoo_standard' or  user.company_id.temp_selection == False or user.company_id.add_watermark == False :
            return result
        else:
            if user.company_id.add_watermark == True and user.company_id.watermark_selection == 'letter_head':
                result = super(IrActionsReport, self)._post_pdf(save_in_attachment, pdf_content=pdf_content, res_ids=res_ids)
                user = self.env['res.users'].browse(self.env.uid)
                watermark = None
                if user.company_id.letter_head:
                    watermark = b64decode(user.company_id.letter_head)
                else:
                    if watermark:
                        watermark = b64decode(watermark)
                   
                if not watermark:
                    return result
                
                pdf = PdfFileWriter()
                pdf_watermark = None 
                watermark_streams = []
                try:
#                     pdf_watermark = PdfFileReader(StringIO(watermark))
                    pdf_watermark = io.BytesIO(watermark)
                    watermark_streams.append(pdf_watermark)
                    pdf_watermark = PdfFileReader(pdf_watermark)
                except PdfReadError:
                    # let's see if we can convert this with pillow
                    try:
                        image = Image.open(io.BytesIO(watermark))
                        pdf_buffer = io.BytesIO()
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                        resolution = image.info.get(
                            'dpi', user.company_id.paperformat_id.dpi or 90
                             
                        )
                        if isinstance(resolution, tuple):
                            resolution = resolution[0]
                        image.save(pdf_buffer, 'pdf', resolution=resolution)
                        pdf_watermark = PdfFileReader(pdf_buffer)
                    except:
                        logger.exception('Failed************ to load watermark')
                 
                if not pdf_watermark:
                    logger.error(
                        'No usable watermark found, got %s...', watermark[:100]
                    )
                    return result
                if pdf_watermark.numPages < 1:
                    logger.error('Your watermark pdf does not contain any pages')
                    return result
                if pdf_watermark.numPages > 1:
                    logger.debug('Your watermark pdf contains more than one page, '
                                 'all but the first one will be ignored')
                    
                
                for page in PdfFileReader(io.BytesIO(result)).pages:
                    watermark_page = pdf.addBlankPage(
                        page.mediaBox.getWidth(), page.mediaBox.getHeight()
                    )
                    watermark_page.mergePage(pdf_watermark.getPage(0))
                    watermark_page.mergePage(page)
                pdf_content = io.BytesIO()
                pdf.write(pdf_content)
                return pdf_content.getvalue()
            else:
                return result
            
