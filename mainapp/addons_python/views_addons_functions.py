from ..models import Puples, Events


def recount_all_peoples_rating() -> None:
    """ Пересчитывает рейтинг всех учеников """
    mass = [i[0] for i in Puples.objects.order_by("-rate").values_list('id')]
    for i in mass:
        pup = Puples.objects.get(id=i)
        pup.rate = sum(map(lambda x: x.event_rate,
                           Events.objects.filter(events__pk=i, check=True)))
        pup.save()