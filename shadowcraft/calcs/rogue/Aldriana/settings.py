from shadowcraft.core import exceptions

class Settings(object):
    # Settings object for AldrianasRogueDamageCalculator.

    def __init__(self, cycle, time_in_execute_range=.35, tricks_on_cooldown=True, response_time=.5, dmg_poison='dp', utl_poison=None, duration=300):
        self.cycle = cycle
        self.time_in_execute_range = time_in_execute_range
        self.tricks_on_cooldown = tricks_on_cooldown
        self.response_time = response_time
        self.dmg_poison = dmg_poison
        self.utl_poison = utl_poison
        self.duration = duration
        if dmg_poison not in (None, 'dp', 'wp'):
            raise exceptions.InvalidInputException(_('You can only choose Deadly(dp) or Wound(wp) as a damage poison'))
        if utl_poison not in (None, 'cp', 'mnp', 'lp', 'pp'):
            raise exceptions.InvalidInputException(_('You can only choose Crippling(cp), Mind-Numbing(mnp), Leeching(lp) or Paralytic(pp) as a non-lethal poison'))


class Cycle(object):
    # Base class for cycle objects.  Can't think of anything that particularly
    # needs to go here yet, but it seems worth keeping options open in that
    # respect.

    # When subclassing, define _cycle_type to be one of 'assassination',
    # 'combat', or 'subtlety' - this is how the damage calculator makes sure
    # you have an appropriate cycle object to go with your talent trees, etc.
    _cycle_type = ''


class AssassinationCycle(Cycle):
    _cycle_type = 'assassination'

    allowed_values = (1, 2, 3, 4, 5)

    def __init__(self, min_envenom_size_non_execute=4, min_envenom_size_execute=5, prioritize_rupture_uptime_non_execute=True, prioritize_rupture_uptime_execute=True, use_garrote='opener'):
        assert min_envenom_size_non_execute in self.allowed_values
        self.min_envenom_size_non_execute = min_envenom_size_non_execute

        assert min_envenom_size_execute in self.allowed_values
        self.min_envenom_size_execute = min_envenom_size_execute

        # There are two fundamental ways you can manage rupture; one is to
        # reapply with whatever CP you have as soon as you can after the old
        # rupture drops; we will call this priorotizing uptime over size.
        # The second is to use ruptures that are the same size as your
        # envenoms, which we will call prioritizing size over uptime. True
        # means the first of these options; False means the second.
        # There are theoretically other things you can do (say, 4+ envenom and
        # 5+ ruptures) but such things are significantly harder to model so I'm
        # not going to worry about them until we have reason to believe they're
        # actually better.
        self.prioritize_rupture_uptime_non_execute = prioritize_rupture_uptime_non_execute
        self.prioritize_rupture_uptime_execute = prioritize_rupture_uptime_execute

        self.use_garrote = use_garrote # Allowed values are 'always' (vanish/shadowmeld on cooldown), 'opener' (once per fight) and 'never'


class CombatCycle(Cycle):
    _cycle_type = 'combat'

    def __init__(self, use_rupture=True, use_revealing_strike='sometimes', ksp_immediately=False):
        self.use_rupture = bool(use_rupture)
        self.use_revealing_strike = use_revealing_strike # Allowed values are 'always' (on all damaging finishers), 'sometimes' (only at 4 cp), and 'never' (guess).
        self.ksp_immediately = bool(ksp_immediately) # Determines whether to KSp the instant it comes off cool or wait until Bandit's Guile stacks up.'


class SubtletyCycle(Cycle):
    _cycle_type = 'subtlety'

    def __init__(self, raid_crits_per_second, clip_recuperate=False, use_hemorrhage='never'):
        self.raid_crits_per_second = raid_crits_per_second
        self.clip_recuperate = clip_recuperate # Determines if you clip the previous recuperate or wait for it to drop before reapplying.
        self.use_hemorrhage = use_hemorrhage # Allowed values are 'always' (main CP generator), 'never' (default to backstab), or a number denoting the interval in seconds between applications.
