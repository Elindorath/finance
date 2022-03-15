#! /usr/bin/env python

import panel as pn


select_area = pn.widgets.Select(name='Select',
                                options=['Biology', 'Chemistry', 'Physics'],
                                size=3)

widgets = pn.Row(select_area)

widgets.servable()
