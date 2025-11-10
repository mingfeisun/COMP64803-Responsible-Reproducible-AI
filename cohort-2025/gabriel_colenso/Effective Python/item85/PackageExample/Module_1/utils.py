def normalise(list):
    return [(x - min(list))/(max(list)-min(list)) for x in list]