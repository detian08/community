# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Web: Odoo Debug Mode",
  "summary"              :  "Allows the admin to enable  debug  in just one click.",
  "category"             :  "web",
  "version"              :  "1.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "http://www.webkul.com",
  "description"          :  """Web: Odoo Debug Mode""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=web_debug",
  "depends"              :  ['web'],
  "data"                 :  ['views/web_debug.xml'],
  "qweb"                 :  ['static/src/xml/web_debug.xml'],
  "images"               :  ['static/description/Banner1.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
