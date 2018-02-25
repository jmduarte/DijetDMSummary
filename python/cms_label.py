import ROOT

# CMS_lumi
#   Initiated by: Gautier Hamel de Monchenault (Saclay)
#   Translated in Python by: Joshua Hardenbrook (Princeton)
#   Updated by:   Dinko Ferencek (Rutgers)
#

cms_text_font   = 61  
extra_text_font = 52 

cms_text_size      = 0.75
cms_text_offset    = 0.1

rel_pos_x    = 0.045
rel_pos_y    = 0.035
rel_extra_dy = 1.2
rel_pos_y_oof = 0.07

extra_text_size      = 0.7
extra_text_dx        = 0.1

def CMSLabel(pad, extra_text="", halign="left", valign="top", in_frame=True):
    # Position
    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    e = 0.025

    pos_x = 0
    if halign == "left":
        pos_x = l + rel_pos_x * (1. - l - r)
    elif halign == "center":
        pos_x =  l + 0.5 * (1. - l - r)
    elif halign == "right":
        pos_x =  1. - r - rel_pos_x * (1. - l - r)

    if in_frame:
        pos_y = 1. - t - rel_pos_y * (1. - t - b)
    else:
        pos_y = 1. - t + rel_pos_y_oof * (1. - t - b)

    # Alignment
    # kHAlignLeft   = 10, kHAlignCenter = 20, kHAlignRight = 30,
    # kVAlignBottom = 1,  kVAlignCenter = 2,  kVAlignTop   = 3
    halign2root = {
        "left":ROOT.kHAlignLeft,
        "center":ROOT.kHAlignCenter,
        "right":ROOT.kHAlignRight,
    }
    valign2root = {
        "top":ROOT.kVAlignTop,
        "center":ROOT.kVAlignCenter,
        "bottom":ROOT.kVAlignBottom,
    }

    # CMS logo
    pad.cd()
    tl_cms_logo = ROOT.TLatex()
    tl_cms_logo.SetNDC()
    tl_cms_logo.SetTextAngle(0)
    tl_cms_logo.SetTextColor(1)
    tl_cms_logo.SetTextFont(cms_text_font)
    tl_cms_logo.SetTextSize(cms_text_size*t)
    tl_cms_logo.SetTextAlign(halign2root[halign] + valign2root[valign])
    tl_cms_logo.DrawLatex(pos_x, pos_y, "CMS")

    # Extra text
    if len(extra_text) >= 1:
        tl_extra_text = ROOT.TLatex()
        tl_extra_text.SetNDC()
        tl_extra_text.SetTextAngle(0)
        tl_extra_text.SetTextColor(1)
        tl_extra_text.SetTextFont(extra_text_font)
        tl_extra_text.SetTextAlign(halign2root[halign] + valign2root[valign])
        tl_extra_text.SetTextSize(extra_text_size * t)

        extra_text_pos_y = 1. - t + rel_pos_y_oof * (1. - t - b) * (1. + extra_text_size / cms_text_size)/2.*0.95

        tl_extra_text.DrawLatex(pos_x + extra_text_dx * (1. - l - r), extra_text_pos_y, extra_text)
