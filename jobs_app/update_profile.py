def update_candidate_profile(user, application):
    name_split = application.name.split()
    user.first_name = name_split[0]
    user.last_name = name_split[-1]
    user.save()
    if not user.candidateprofile.resume:
        user.candidateprofile.resume = application.resume
        user.candidateprofile.name = application.name
        user.candidateprofile.skills = ','.join(set(user.candidateprofile.skills.split(',')).union(set(application.skills.split())))
        user.candidateprofile.sites = ',',join(set(user.candidateprofile.sites.split(',')).union(set(application.sites.split())))
        user.candidateprofile.save()
