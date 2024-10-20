---
layout: band
---
## Upcoming Rehearsals and Actions

### HONK! Logistics Meeting:
Monday Sept. 30th @ 4pm. (link in NM4P HONK! chat description)

### Regular Rehearsals:
TODO: Schedule next rehearsal

## Rep List
### Current Rep

{% for song in site.songs %}
{% if song.status == "current" %}
- [{{song.title}}]({{song.url | relative_url}})
{% endif %}
{% endfor %}

### Songs we're currently learning
We have arrangements for these, and are working them up to play out.

{% for song in site.songs %}
{% if song.status == "learning" %}
- [{{song.title}}]({{song.url | relative_url}})
{% endif %}
{% endfor %}

### Songs we want to play
We don't have arrangements for these yet, but they're on our radar.
If you want to make an arrangement that'd be cool.

{% for song in site.songs %}
{% if song.status == "future" %}
- [{{song.title}}]({{song.url | relative_url}})
{% endif %}
{% endfor %}

## Resources

[Chants with Arabic Rhythms](chants_and_rhythms.html)

[Maqam World](https://maqamworld.com/)
