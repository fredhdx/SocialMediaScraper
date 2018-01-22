def tempalte_PinkElegance(timecards, ignore_retweet=True):
    """ A builder for template body: PinkElegance
        Abandoned for incomplet js generation
        Source: https://codepen.io/mo7hamed/pen/dRoMwo
    """
    # build body
    body_string = ""
    for i in range(0, len(timecards.content)):

        if ignore_retweet and timecards.content[i].startswith('转发'):
            continue
        else:
            meta_string = ("点赞：" + str(timecards.meta[i]['up_num']) + " 转发：" + str(timecards.meta[i]['retweet_num'])
                            + " 评论：" + str(timecards.meta[i]['comment_num']))
            body_string = body_string + "<li>\n" + "<span></span>\n"
            body_string = (body_string + "<div class=\"title\">" + timecards.time[i][:4] + "</div>\n"
                            + "<div class=\"info\">" + timecards.content[i] + "</div>\n"
                            + "<div class=\"name\">" + meta_string + "</div>\n"
                            + "<div class=\"time\">" + "\n<span>" + timecards.time[i][4:6] + "月" + timecards.time[i][6:8] + "日</span>\n"
                            + "<span>" + timecards.time[i][8:10] + ":" + timecards.time[i][10:12] + "</span>\n"
                            + "</div>")
    return body_string

def template_FlexBox(timecards, ignore_retweet=True):
    """ A builder for template: FlexBox
        CSS broekn somehow
        Source: https://codepen.io/paulhbarker/pen/apvGdv
    """
    body_string = ""
    for i in range(0, len(timecards.content)):
        if ignore_retweet and timecards.content[i].startswith('转发'):
            continue
        else:
            meta_string = ("点赞：" + str(timecards.meta[i]['up_num']) + " 转发：" + str(timecards.meta[i]['retweet_num'])
                            + " 评论：" + str(timecards.meta[i]['comment_num']))
            body_string = (body_string
                            + "<div class=\"demo-card weibo-card\">\n"
                            + "<div class=\"head\">\n"
                            + "<div class=\"number-box\">\n"
                            + "<span>" + timecards.time[i][6:8] + "</span>\n"
                            + "</div>"
                            + "<h2><span class=\"small\">" + timecards.time[i][:4] + "年" + timecards.time[i][4:6] + "月" + "</span>"
                                + timecards.content[i][:8] + "</h2>\n"
                            + "</div>\n"
                            + "<div class=\"body\">\n"
                            + "<p>" + timecards.content[i][8:] + "\n\n" + meta_string + "</p>\n"
                            # + "<img src=\"" + timecards.img_src[i] + "\">\n"
                            + "</div>\n</div>\n\n")
    return body_string

def template_PinkStar(timecards, weibo_url, ignore_retweet=True):
    """ A builder for template: FlexBox

        Source: https://codepen.io/itbruno/pen/KwarLp
    """

    icon_string_star = ('<div class="timeline-icon">\n'
                        + '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" '
                        + 'xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="21px" '
                        + 'height="20px" viewBox="0 0 21 20" enable-background="new 0 0 21 20" xml:space="preserve">\n'
					    + '<path fill="#FFFFFF" d="M19.998,6.766l-5.759-0.544c-0.362-0.032-0.676-0.264-0.822-0.61l-2.064-4.999\n'
	                    + 'c-0.329-0.825-1.5-0.825-1.83,0L7.476,5.611c-0.132,0.346-0.462,0.578-0.824,0.61L0.894,6.766C0.035,6.848-0.312,7.921,0.333,8.499\n'
	                    + 'l4.338,3.811c0.279,0.246,0.395,0.609,0.314,0.975l-1.304,5.345c-0.199,0.842,0.708,1.534,1.468,1.089l4.801-2.822\n'
	                    + 'c0.313-0.181,0.695-0.181,1.006,0l4.803,2.822c0.759,0.445,1.666-0.23,1.468-1.089l-1.288-5.345\n'
	                    + 'c-0.081-0.365,0.035-0.729,0.313-0.975l4.34-3.811C21.219,7.921,20.855,6.848,19.998,6.766z" />\n'
				        + '</svg>\n'
			            + '</div>\n')

    icon_string_book = ('<div class="timeline-icon">\n'
                        + '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" '
                        + '<g>'
                        + 'xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="21px" '
                        + 'height="20px" viewBox="0 0 21 20" enable-background="new 0 0 21 20" xml:space="preserve">\n'
					    + '<path fill="#FFFFFF" d="M17.92,3.065l-1.669-2.302c-0.336-0.464-0.87-0.75-1.479-0.755C14.732,0.008,7.653,0,7.653,0v5.6\n'
                        + 'c0,0.096-0.047,0.185-0.127,0.237c-0.081,0.052-0.181,0.06-0.268,0.02l-1.413-0.64C5.773,5.183,5.69,5.183,5.617,5.215l-1.489,0.65\n'
                        + 'c-0.087,0.038-0.19,0.029-0.271-0.023c-0.079-0.052-0.13-0.141-0.13-0.235V0H2.191C1.655,0,1.233,0.434,1.233,0.97\n'
                        + 'c0,0,0.025,15.952,0.031,15.993c0.084,0.509,0.379,0.962,0.811,1.242l2.334,1.528C4.671,19.905,4.974,20,5.286,20h10.307\n'
                        + 'c1.452,0,2.634-1.189,2.634-2.64V4.007C18.227,3.666,18.12,3.339,17.92,3.065z M16.42,17.36c0,0.464-0.361,0.833-0.827,0.833H5.341\n'
                        + 'l-1.675-1.089h10.341c0.537,0,0.953-0.44,0.953-0.979V2.039l1.459,2.027V17.36L16.42,17.36z" />\n'
                        + '</g>\n'
				        + '</svg>\n'
			            + '</div>\n')



    body_string = ""
    RightDirection = False
    for i in range(0, len(timecards.content)):
        if ignore_retweet and timecards.content[i].startswith('转发'):
            continue
        else:
            meta_string = ("点赞：" + str(timecards.meta[i]['up_num']) + " 转发：" + str(timecards.meta[i]['retweet_num'])
                            + " 评论：" + str(timecards.meta[i]['comment_num']))
            time_string = (timecards.time[i][:4] + '年' + timecards.time[i][4:6] + '月' + timecards.time[i][6:8] + '日'
                            + '      ' + timecards.time[i][8:10] + ':' + timecards.time[i][10:12])

            body_string = (body_string
                            + '<div class="timeline-item">\n'
                            + (icon_string_book if RightDirection else icon_string_star + '\n')
                            + ('<div class="timeline-content right">\n' if RightDirection else '<div class="timeline-content">\n')
                            + '<h2>' + time_string + '</h2>\n'
                            + '<p>' + timecards.content[i] + '</p>\n'
                            + '<a href="' + weibo_url + '" class="btn">' + meta_string + "</a>"
                            + '</div>'
                            + '</div>')

            RightDirection = not RightDirection

    return body_string
