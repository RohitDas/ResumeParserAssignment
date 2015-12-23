import re, nltk

class SkillsExtraction:
    """
        This class contains the functionalities to extract the skills
    """
    def __init__(self,skill_section):
        self.skill_section = skill_section

    def isSkillSection(self,line):
        """
        :param line: Line in a paragraph
        :return: Boolean , whether it is a skill section or not.
        """

        if "SKILL" in line or "PROFICIENCY" in line or "EXPERTISE" in line:
            return True
        else:
            return False

    def get_Skills(self):
        """
                :return: Return a list of skills.
        """
        #Search for a colon or a semocolon and separate the left and right parts
	    
	skillsection = []
        for line in self.skill_section:
             if line.strip():
                findallobjs = re.findall('(.*)(:\s*-|:)\s*(.*)',line)
                if findallobjs:
                    for (subsection,colon,line) in findallobjs:
                            skillindiv = re.split('\t|,',line)
                            if skillindiv:
                                skillsection += skillindiv
                else:
                    skillindiv = re.split('\t|,',line)
                    if skillindiv:
                        skillsection += skillindiv
        skillsection = [x.strip() for x in skillsection if x.strip()]
	derived_skills = self.deriveSkills(skillsection)
	post_processed_skill_list = self.post_process_skills(derived_skills)
        #Pos Tag the words.
        return post_processed_skill_list


    def deriveSkills(self,skill_list):
        """
            Function to modify skill sections , level 2
        """
        # regx = re.compile('.*\s(in|at|with|as)\s(.*)',re.IGNORECASE)
        result = []
        for skill in skill_list:
            relevant_tags = []
            tokens = skill.split(" ")
            if len(tokens) > 3:
                pos_tagged_tokens = nltk.pos_tag(tokens)
                for skill, pos_tag in pos_tagged_tokens:
                    if pos_tag in ["NN","NNS","NNP","NNPS","VB","VBD","VBG","VBN"]:
                        relevant_tags.append((skill,pos_tag))
                a,b = zip(*relevant_tags)
                result.append(" ".join(a))
            else:
                result.append(" ".join(tokens))
        return result

    def post_process_skills(self,skill_list):
        """
            Post Process the Skill list and remove junk
        """
        new_skill_list = []
        for skill in skill_list:
            skill = re.sub('^\d+',"",skill)
            skill = re.sub('\.\s*$',"",skill)
            new_skill_list.append(skill)
        return new_skill_list
