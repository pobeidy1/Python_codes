def click_to_crop_img(img):
    from matplotlib.widgets import RectangleSelector
    import matplotlib.pyplot as plt

    
    def line_select_callback(eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))
    
    
    def toggle_selector(event):
        print(' Key pressed.')
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            print(' RectangleSelector deactivated.')
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            print(' RectangleSelector activated.')
            toggle_selector.RS.set_active(True)
    
    
    fig, current_ax = plt.subplots()                 # make a new convas  
    current_ax.imshow(img)
    current_ax.title.set_text('Select foreground ROI and press q')
    print("\n      click  -->  release")
    
    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1, 3],  # don't use middle button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=True)
    
    plt.connect('key_press_event', toggle_selector)
    plt.show()
    
    plt.pause(10)
    
    plt.close('all')
    
    
    # Get the mask coordinates
    start=(int(toggle_selector.RS.extents[2]),  
    int(toggle_selector.RS.extents[1]))
    end=(int(toggle_selector.RS.extents[3]), 
    int(toggle_selector.RS.extents[0]))
    
    x1 =end[1]
    y1=start[0]
    x2=start[1]
    y2=end[0]
    
    #step2) crop the image using the x1,x2,y1,y2
    
    w=x2-x1
    h=y2-y1
    
    cropped_image = img[y1:y1+h,x1:x1+w]
    plt.imshow(cropped_image)
    #plt.savefig(cropped_image+'.png', format='png', dpi=100)

    import pickle

    a = 3; b = [11,223,435];
    pickle.dump([cropped_image], open("trial.p", "wb"))

    #c,d = pickle.load(open("trial.p","rb"))

    #print(c,d) ## To verify    
    return cropped_image
