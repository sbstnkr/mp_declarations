from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import re
import string


class Declaration:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.polish_letters = 'ĄĆĄĆĘŁŃÓŚŹŻąćęłńóśźż'

    def get_text(self):
        doc = convert_from_path(self.pdf_file)

        for page_number, page_data in enumerate(doc):
            if page_number == 0:
                file_name = f'page_{page_number}.png'
                page_data.save(file_name, 'PNG')

                image_file = Image.open(file_name)

                txt_old = pytesseract.image_to_string(image_file, lang='pol')\
                    .replace('Kliknij tutaj, aby wprowadzić tekst.', '')\
                    .replace('\n \n', '\n')\
                    .replace('podpisanyfa)', 'podpisany(a)')

                #print(txt_old)

                #maiden = txt_old.lower().split('z d. ')[1].split('\n')[0]

                #txt_old = txt_old.lower().replace(maiden, '').replace(' z d. ', '\n')
                #print(txt_old)

                text_listed = txt_old.split('\n')

                txt = ""
                for item in text_listed:
                    if item:
                        txt += item + '\n'

                #print(txt)

                basic_info = txt.partition('Ja,')[2].partition('lub funkcja')[0]
                #print(basic_info)

                wealth_info = txt.partition('Zasoby pieni')[2].partition('Dom')[0]
                #print(wealth_info)

                return basic_info.lower(), wealth_info

    def get_name(self):
        try:
            name = re.sub(f'[^{self.polish_letters}A-Za-z -]+', '',
                            re.search('podpisany\(a\), (.*)\n', self.get_text()[0]).group(1)).strip().title()
        except AttributeError:
            name = re.sub(f'[^{self.polish_letters}A-Za-z -]+', '',
                          re.search('podpisany, (.*)\n', self.get_text()[0]).group(1)).strip().title()

        print(name)

    def get_dob(self):
        try:
            dob = re.sub(f'[^{self.polish_letters}A-Za-z0-9 .-]+', '',
                            re.search('\(a\) (.*) r\. w', self.get_text()[0]).group(1)).strip()
        except AttributeError:
            try:
                dob = re.sub(f'[^{self.polish_letters}A-Za-z0-9 .-]+', '',
                             re.search('\(a\) (.*)r\. w', self.get_text()[0]).group(1)).strip()

            except AttributeError:
                try:
                    dob = re.sub(f'[^{self.polish_letters}A-Za-z0-9 .-]+', '',
                                 re.search('\(a\) (.*) w ', self.get_text()[0]).group(1)).strip()

                except AttributeError:
                    dob = re.sub(f'[^{self.polish_letters}A-Za-z0-9 .-]+', '',
                                 re.search('urodzony (.*)r\. w', self.get_text()[0]).group(1)).strip()

        print(dob)

    def get_pob(self):
        try:
            pob = re.sub(f'[^{self.polish_letters}A-Za-z -]+', '',
                            re.search('r\. w (.*)\n', self.get_text()[0]).group(1)).strip().title()
        except AttributeError:
            pob = re.sub(f'[^{self.polish_letters}A-Za-z -]+', '',
                         re.search(' w (.*)', self.get_text()[0].split('\n')[2]).group(1)).strip().title()

        print(pob)

    def get_position(self):
        if '\nposeł na Sejm RP\n' or '\nPoseł na Sejm RP\n' in self.get_text()[0]:
            position = 'Poseł na Sejm RP'
        else:
            position = self.get_text()[0].split('\n')[3].strip().title()

        print(position)

    def get_pln_money(self):
        try:
            pln_money = re.sub(f'[^{self.polish_letters}^0-9,. A-Za-z]+', '',
                               re.search('polskiej: (.*)\n', self.get_text()[1]).group(1)).strip()

            if all(i in string.punctuation for i in pln_money):
                pln_money = self.get_text()[1].split('\n')[2].strip()

        except AttributeError:
            pln_money = self.get_text()[1].split('\n')[2].strip()

        print(pln_money)

    def get_foreign_money(self):
        try:
            foreign_money = re.sub(f'[^{self.polish_letters}^0-9,. A-Za-z]+', '',
                               re.search('obcej: (.*)\n', self.get_text()[1]).group(1)).strip()

            if all(i in string.punctuation for i in foreign_money):
                foreign_money = self.get_text()[1].split('\n')[2].strip()

        except AttributeError:
            foreign_money = self.get_text()[1].split('\n')[2].strip()

        print(foreign_money)


pdf_file = 'OSW91_159.pdf'

declaration = Declaration(pdf_file=pdf_file)
declaration.get_name()
declaration.get_dob()
declaration.get_pob()
declaration.get_position()
declaration.get_pln_money()







