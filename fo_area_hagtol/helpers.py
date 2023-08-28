

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.style as style


style.use('fivethirtyeight')

def style_fig(fig):
    fig.tick_params(axis = 'both', which = 'major', labelsize = 18)
    fig.axhline(y = 0, color = 'black', linewidth = 1.3, alpha = .7)
    fte_graph.text(x = 1965.8, y = -7,
    s = ' ©DATAQUEST Source: National Center for Education Statistics',fontsize = 14, color = '#f0f0f0', backgroundcolor = 'grey')

def box_plot_2(percentiles, *args, **kwargs):
    """
    Generates a customized boxplot based on the given percentile values
    """
    redraw = True

    labels = []
      
    f, a = plt.subplots()
    f.subplots_adjust(bottom=0.2)
    box_plot = a.boxplot([[-9, -4, 2, 4, 9],]*len(percentiles), *args, **kwargs) 
    # Creates len(percentiles) no of box plots
    
    min_y, max_y = float('inf'), -float('inf')
    
    for box_no, (label,
                 q1_start, 
                 q2_start,
                 q3_start,
                 q4_start,
                 q4_end,
                 fliers_xy) in enumerate(percentiles):
        
    
        labels.append(label)
        # Lower cap
        box_plot['caps'][2*box_no].set_ydata([q1_start, q1_start])
        # xdata is determined by the width of the box plot

        # Lower whiskers
        box_plot['whiskers'][2*box_no].set_ydata([q1_start, q2_start])

        # Higher cap
        box_plot['caps'][2*box_no + 1].set_ydata([q4_end, q4_end])

        # Higher whiskers
        box_plot['whiskers'][2*box_no + 1].set_ydata([q4_start, q4_end])

        # Box
        box_plot['boxes'][box_no].set_ydata([q2_start, 
                                             q2_start, 
                                             q4_start,
                                             q4_start,
                                             q2_start])
        
        # Median
        box_plot['medians'][box_no].set_ydata([q3_start, q3_start])

        # Outliers
        if fliers_xy is not None and len(fliers_xy[0]) != 0:
            # If outliers exist
            box_plot['fliers'][box_no].set(xdata = fliers_xy[0],
                                           ydata = fliers_xy[1])
            
            min_y = min(q1_start, min_y, fliers_xy[1].min())
            max_y = max(q4_end, max_y, fliers_xy[1].max())
            
        else:
            min_y = min(q1_start, min_y)
            max_y = max(q4_end, max_y)
                    
        # The y axis is rescaled to fit the new box plot completely with 10% 
        # of the maximum value at both ends
        a.set_ylim([min_y*1.1, max_y*1.1])
    a.set_xticklabels(labels, rotation = 45)
    # If redraw is set to true, the canvas is updated.
    #if redraw:
    #    ax.figure.canvas.draw()
        
    return box_plot

