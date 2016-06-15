#Caba additions
from header_common import reg5, reg1
overlay_var = reg5
buttons_begin = "$g_presentation_obj_name_kingdom_1"
mouse_over    = "$g_presentation_obj_name_kingdom_2"
presobj_array = "trp_temp_array_a"
#Caba end

## overlay types
xgm_ov_none         = 0         # unused
xgm_ov_text         = 1         # unused
xgm_ov_line         = 2         # this just creates a horizontal divider
xgm_ov_checkbox     = 11
xgm_ov_numberbox    = 12
xgm_ov_combolabel   = 13
xgm_ov_combobutton  = 14
xgm_ov_slider       = 15
xgm_ov_title        = 16

## size of base pane for option properties
xgm_mod_options_pane_width = 550
#xgm_mod_options_pane_width = 600
xgm_mod_options_pane_height = 630
xgm_mod_options_pane_posx = 50
xgm_mod_options_pane_posy = 50

## option property row in base pane
xgm_mod_options_property_width  = xgm_mod_options_pane_width
xgm_mod_options_property_height = 50
xgm_mod_options_property_posx   = 0

## option property value in a row
xgm_mod_options_property_value_width    = 250
xgm_mod_options_property_value_height   = 50
xgm_mod_options_property_value_posx     = xgm_mod_options_property_width - xgm_mod_options_property_value_width/2 # centered

## option property label in a row
xgm_mod_options_property_label_width = xgm_mod_options_property_width - xgm_mod_options_property_value_width
xgm_mod_options_property_label_height = 50
xgm_mod_options_property_label_posx = xgm_mod_options_property_posx # left


## size of line in base pane
xgm_mod_options_line_width = xgm_mod_options_pane_width
xgm_mod_options_line_height = 2
xgm_mod_options_line_posx = 0
xgm_mod_options_line_offsetx = xgm_mod_options_line_width/2
xgm_mod_options_line_offsety = xgm_mod_options_property_height/2


## offsets and size
xgm_ov_numberbox_base_width = 64
xgm_ov_numberbox_base_height = 28
xgm_ov_numberbox_scalex = 1000
xgm_ov_numberbox_scaley = 1000
xgm_ov_numberbox_width = xgm_ov_numberbox_base_width * xgm_ov_numberbox_scalex / 1000
xgm_ov_numberbox_height = xgm_ov_numberbox_base_height * xgm_ov_numberbox_scaley / 1000
xgm_ov_numberbox_offsetx = - xgm_ov_numberbox_width/2
xgm_ov_numberbox_offsety = -xgm_ov_numberbox_height/2

xgm_ov_checkbox_base_width = 18
xgm_ov_checkbox_base_height = 18
xgm_ov_checkbox_scalex = 1000#1500
xgm_ov_checkbox_scaley = 1000#1500
xgm_ov_checkbox_width = xgm_ov_checkbox_base_width * xgm_ov_checkbox_scalex / 1000
xgm_ov_checkbox_height = xgm_ov_checkbox_base_height * xgm_ov_checkbox_scaley / 1000
xgm_ov_checkbox_offsetx = - xgm_ov_checkbox_width/2
xgm_ov_checkbox_offsety = -xgm_ov_checkbox_height/2

xgm_ov_combolabel_base_width = 328
xgm_ov_combolabel_base_height = 28
xgm_ov_combolabel_scalex = 700#750
xgm_ov_combolabel_scaley = 800#1000
xgm_ov_combolabel_width = xgm_ov_combolabel_base_width * xgm_ov_combolabel_scalex / 1000
xgm_ov_combolabel_height = xgm_ov_combolabel_base_height * xgm_ov_combolabel_scaley / 1000
xgm_ov_combolabel_offsetx = xgm_ov_combolabel_base_width/2 - xgm_ov_combolabel_width/2
xgm_ov_combolabel_offsety = -xgm_ov_combolabel_height/2

xgm_ov_combobutton_base_width = 216
xgm_ov_combobutton_base_height = 28
xgm_ov_combobutton_scalex = 700#750
xgm_ov_combobutton_scaley = 800#1000
xgm_ov_combobutton_width = xgm_ov_combobutton_base_width * xgm_ov_combobutton_scalex / 1000
xgm_ov_combobutton_height = xgm_ov_combobutton_base_height * xgm_ov_combobutton_scaley / 1000
xgm_ov_combobutton_offsetx = xgm_ov_combobutton_base_width/2 - xgm_ov_combobutton_width/2
xgm_ov_combobutton_offsety = -xgm_ov_combobutton_height/2


xgm_ov_slider_base_width = 248
xgm_ov_slider_base_height = 28
xgm_ov_slider_scalex = 750
xgm_ov_slider_scaley = 1000
xgm_ov_slider_width = xgm_ov_slider_base_width * xgm_ov_slider_scalex / 1000
xgm_ov_slider_height = xgm_ov_slider_base_height * xgm_ov_slider_scaley / 1000
xgm_ov_slider_offsetx = xgm_ov_slider_base_width/2 - xgm_ov_slider_width/2
xgm_ov_slider_offsety = -xgm_ov_slider_height/2

## WINDYPLAINS+ ## - Title Bar
xgm_ov_titlebar_offsetx = xgm_mod_options_pane_width/2
## WINDYPLAINS- ##
