.. currentmodule:: pyzork

Tips
=====
There are many little tips and tricks you can use in the library to get a better use of it.

Infinity
----------
Infinity within the library is very useful, since the library doesn't natively support permanent durations
you can instead make the duration infinite, using python `math.inf`. For example, a debuff which lasts forever
would look like::
    
    from pyzork import Modifier, StatEnum
    import math
    
    @Modifier.add_buff(duration=math.inf, stat=StatEnum.defense)
    def InfiniteDebuff(modifier, target):
        return -3

This would permanently reduce the defense of the target by 3. This can be interesting to simulate wounds or other long term events.
