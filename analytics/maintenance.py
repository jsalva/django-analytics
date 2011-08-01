from django.utils.translation import ugettext as _

from analytics import settings
from analytics.options import Statistic


def list_gadgets():
    """
    Prints all of the available gadgets and their corresponding statistics.
    """
    print ""
    print "Gadget\t\t\tStatistics"
    print "------\t\t\t----------"
    for gadget in gadgets.get_gadgets():
        print u"%s\t\t%s" % (gadget, ', '.join([u'%s' % s.get_label() for s in gadget.stats]))

    print ""



def ensure_list(v):
    """
    Makes sure that the given value is a list.
    """
    return list(v) if getattr(v, '__iter__', False) else [v]



def get_statistic_by_name(stat_name):
    """
    Fetches a statistics based on the given class name. Does a look-up
    in the gadgets' registered statistics to find the specified one.
    """

    for stat in get_statistic_models():
        if stat.__name__ == stat_name:
            return stat

    raise Exception, _("%(stat)s cannot be found.") % {'stat': stat_name}


def get_statistic_models():
    from django.db.models import get_models
    import inspect
    
    stats = []
    for model in get_models():
        if Statistic in inspect.getmro(model):
            stats.append(model)

    return stats
        

def calculate_statistics(frequency):
    """
    Calculates all of the metrics associated with the registered gadgets.
    """
    frequency = ensure_list(frequency)

    for stat in get_statistic_models():
        for f in frequency:
            print "Calculating %s (%s)..." % (stat, settings.STATISTIC_FREQUENCY_DICT[f])
            stat.calculate(f)

def reset_statistics(stat, frequencies, reset_cumulative):
    """
    Resets the specified statistic's data (deletes it) for the given
    frequency/ies.
    """

    stats = gadgets.get_active_stats() if stat == 'ALL' else ensure_list(stat)
    frequencies = ensure_list(frequencies)

    for s in stats:
        for f in frequencies:
            if not s.is_cumulative() or reset_cumulative:
                print "Resetting %s (%s)..." % (s, settings.STATISTIC_FREQUENCY_DICT[f])
                s.objects.filter(frequency=f).delete()
            elif s.is_cumulative() and not reset_cumulative:
                print "Skipping %s because it is cumulative." % s


