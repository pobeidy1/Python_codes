import slide_data
from pptx import Presentation
from pptx.util import Inches

slide_data = {
    "slide1": {
        "title": "Slide 1 Title",
        "subtitle": "Slide 1 Subtitle",
        "subtitle_bullet_list": ["Item 1", "Item 2", "Item 3"],
        "figure": "slide1.png"
    },
    "slide2": {
        "title": "Slide 2 Title",
        "subtitle": "Slide 2 Subtitle",
        "subtitle_bullet_list": ["Item A", "Item B", "Item C"],
        "figure": "slide2.png"
    }
}
# print(dir(slide_data))
# print(slide_data)
# slides = list(slide_data.items())
# # Create a new presentation object
# prs = Presentation()

import pptx
import slide_data

# Open the presentation
prs = pptx.Presentation()

# Loop through the slides
for slide_num, slide_info in slide_data():
    # Create a new slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Add the slide title
    title = slide.shapes.title
    title.text = slide_info["title"]

    # Add the slide subtitle
    subtitle = slide.placeholders[1]
    subtitle.text = slide_info["subtitle"]

    # Add the bullet points to the slide
    bullet_slide_layout = slide.slide_layout
    bullet_shape = bullet_slide_layout.shapes.placeholders[1].text_frame
    tf = bullet_shape.text_frame
    for point in slide_info["bullet_list"]:
        tf.add_paragraph().text = point

    try:
        # Add the slide figure
        picture = slide.shapes.add_picture(slide_info["figure"], left, top, height, width)
    except FileNotFoundError:
        print("Error: figure file not found for slide {}".format(slide_num))

# Save the presentation
prs.save("presentation.pptx")
