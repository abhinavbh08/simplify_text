from dataclasses import replace
import re
from numpy import full
from abbreviations import schwartz_hearst

def replace_abbreviation(sentence, dkt):
    all_occurences = {}
    for word, full_form in dkt.items():
        occurences_list = [m.start() for m in re.finditer(rf"\b{word}\b", sentence)]
        for occ in occurences_list:
            if occ>0 and sentence[occ-1]=="(":
                continue
            all_occurences[occ]  = [word, full_form]
    all_occurences = dict(sorted(all_occurences.items()))

    start_idx = 0
    edited_sentence = ''
    for idx, (word, full_form) in all_occurences.items():
        # parts = concept[8].split('/')
        end_idx = idx
        edited_sentence += sentence[start_idx: end_idx]
        
        edited_sentence += full_form
        start_idx = end_idx + len(word)

    # If no concepts are found, copy everything!
    if start_idx != 0:
        edited_sentence += sentence[start_idx: len(sentence)]
    else:
        edited_sentence = sentence

    return edited_sentence
# text =  """
# We assessed bleb morphology and the intraocular pressure (IOP)-lowering effect of trabeculectomy with ologen compared to mitomycin C (MMC) in juvenile open-angle glaucoma (JOAG).This is a prospective interventional comparative study conducted on 40 eyes (20 patients) with medically uncontrolled JOAG, randomly operating one eye for trabeculectomy with ologen (group A: 20 eyes) and the other with MMC (group B: 20 eyes). IOP measurement, SITA standard perimetry, and spectral domain optical coherence tomography (OCT) for retinal nerve fiber layer (RNFL) thickness were all done pre- and postoperatively. Postoperative blebs were assessed clinically using the Moorfields bleb grading system (MBGS) and anterior segment OCT (AS-OCT). All patients were examined for up to 1 year postoperatively. The mean postoperative IOP was statistically significantly lower than the mean preoperative IOP at each follow-up in each group. At 1 year, the mean postoperative IOP was significantly lower in group A. According to the MBGS, blebs with an ologen implant showed significantly better scoring than those with MMC. AS-OCT showed that ologen-induced blebs had significantly more fluid-filled spaces, cleavage planes, and less fibrosis. Ologen resulted in a lower long-term postoperative IOP, a better bleb morphology, and fewer complications. Our results suggest that ologen may be a useful alternative to MMC in JOAG.
# """

# pairs = schwartz_hearst.extract_abbreviation_definition_pairs(doc_text=text, most_common_definition=True)
# # print(pairs)

# sentence = "The mean postoperative IOP was statistically significantly lower than the mean preoperative IOP at each follow-up in each group. At 1 year, the mean postoperative IOP was significantly lower in group A. According to the MBGS, blebs with an ologen implant showed significantly better scoring than those with MMC."
# replace_abbreviation(sentence, pairs)

# sentence = "This is cool?"
# sentence = re.sub(r'\bcool\b', 'robert', sentence)
# print(sentence)
# print([m.start() for m in re.finditer(r"\bcool\b", sentence)])