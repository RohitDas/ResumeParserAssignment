import re

class TextExtraction:
    """This class reads json element by element and considers any two lines
    having vertical distance more than 1.5 times of line height as paragraph break"""

    def __init__(self, jsoncontent):
        if jsoncontent:
            self.jsontext = jsoncontent[jsoncontent.index("text")+7:]
            self.jsontext = self.jsontext.replace("\u0026lt;", "<")
            self.jsontext = self.jsontext.replace("\u0026gt;", ">")
            self.jsontext = self.jsontext.replace("\u0027", "'")
            self.jsontext = self.jsontext.replace("\u0026quot", "")
            self.jsontext = self.jsontext.replace("\u0026amp;", "&")
            self.jsontext = self.jsontext.replace("\u0026amp;", "&")
        else:
            self.jsontext = None

    def getLines(self):
       """
            return: Return a list of lines.
       """
       regx = re.compile('"top":(.*?),"left":(.*?),"width":(.*?),"height":(.*?),"font":(.*?),"data":"(.*?)"}')
       try:
            if self.jsontext:
                itr = regx.finditer(self.jsontext)
                first_obj = itr.next()
                previous_word_top = int(first_obj.group(1))
                previous_line_height = int(first_obj.group(4))
                previous_padding = int(first_obj.group(2))
                current_line = []
                previous_font = first_obj.group(5)
                lines = []
                superscript_detected = False
                if first_obj.group(6).strip():
                    current_line.append(first_obj.group(6).strip())
                for i in itr:
                    current_word_top = int(i.group(1))
                    current_line_height = int(i.group(4))
                    current_pad = int(i.group(2))
                    current_text = i.group(6).strip()
                    current_font = i.group(5)
                    #If current text is null, skip and start with the next iteration.
                    if current_text.strip() == "":
                        continue
                    # Case to check for a colon.
                    if current_word_top == previous_word_top:
                        current_line.append(current_text)
                        previous_font = current_font
                    else:

                        #Previous line empty Feature.
                        lineSpace = current_word_top - previous_word_top
                        if abs(lineSpace) > (previous_line_height*2):
                            line = ' '.join(current_line)
                            line = ''.join(i for i in line if ord(i) < 128)
                            lines.append((line, previous_font, previous_padding))
                            lines.append((" ", previous_font, previous_padding))
                        else:
                            #This step is added to check for superscript and subscript and we consider it as a text on the same line.
                            if re.search("(st|ST|nd|ND|rd|RD|th|TH)",current_text) and current_line_height != previous_line_height:
                                current_line.append(current_text)
                                superscript_detected = True
                            elif superscript_detected and current_line_height != previous_line_height:
                                current_line.append(current_text)
                                superscript_detected = False
                            else:
                                line = ' '.join(current_line)
                                line = ''.join(i for i in line if ord(i) < 128)
                                lines.append((line,previous_font,previous_padding))

                        previous_line_height = current_line_height
                        previous_word_top = current_word_top
                        current_line = []
                        current_line.append(current_text)
                        previous_font = current_font
                        previous_padding = current_pad

                return  lines
            else:
                return None
       except Exception as e:
            print e.message()
            return "Error Detected"



