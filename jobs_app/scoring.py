edu_score = {
    1: 0.2,
    2: 0.2,
    3: 0.3,
    4: 0.6,
    5: 0.9,
}

tier1_colleges = [
    'Indian institute of technology',
    'National institute of technology',

    'Delhi technical university',
    'Indian institute of information technology',
]

tier2_colleges = [
    'Birla institute of technology',
    'Vellore institute of technology',
    'Manipal universiy',
    'SRM University'
    'College of Engineering, Pune'
    'Thapar Institute of Engineering and Technology, Patiala'
    'Jaypee Institute of Information Technology'
]

def _college_score(education):
    if education.level > 2:
        if any(coll.lower() in education.college.lower() for coll in tier1_colleges):
            return 0.9
        elif any(coll.lower() in education.college.lower() for coll in tier2_colleges):
            return 0.6
        else:
            return 0.3
    return 0

def _percent_score(education):
    if education.level in [1,2]:
        if education.percent >=85:
            return 0.9
        elif 70 <= education.percent < 85:
            return 0.6
        elif 60 <= education.percent < 70:
            return 0.3
        return 0
    
    elif education.level in [3,4,5]:
        if education.percent >=75:
            return 0.9
        elif 65 <= education.percent < 75:
            return 0.6
        elif 60 <= education.percent < 65:
            return 0.3
        return 0
    
    return 0

def get_score_for_user_application(user, job_application):
    score = 0.0
    # score the maximum education level
    max_edu = None
    max_edu_lvl = 0
    for edu in user.education_set.all():
        score += _college_score(edu)
        score += _percent_score(edu)
        if edu.level > max_edu_lvl:
            max_edu = edu
            max_edu_lvl = edu.level

    if max_edu:
        score += edu_score[max_edu.level]
    
    # score the experience years

    exp_years = 0
    for exp in user.experience_set.all():
        exp_years += exp.experience_years
    
    if exp_years >= 5:
        score += 0.9
    elif 2 <= exp_years < 5:
        score += 0.6
    elif exp_years == 1:
        score += 0.3
    
    # score on number of skills in job application
    skills = job_application.skills.split(',')
    if len(skills)>5:
        score += 0.9
    elif 3 <= len(skills) <=5:
        score += 0.6
    elif 1 <= len(skills) <=2:
        score += 0.3
    
    # score on video
    if job_application.video_token:
        score += 0.9
    
    # score on country
    if user.candidateprofile.country.lower() == "india":
        score += 0.9
    
    return float("{0:.2f}".format(score))