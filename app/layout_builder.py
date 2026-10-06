def build_comic_layout(outline, story, images):
    by_num={x["panel_number"]:x for x in story}
    return [{**p,"image":images[i],**by_num.get(p["panel_number"],{})} for i,p in enumerate(outline)]
