---
---
## Upcoming Rehearsals and Actions

### HONK! Rehearsals (location TBD):

1. Sunday 9/22, 3-5pm
2. Sunday 9/29, 3-5pm

### Regular Rehearsals:

Thursday 9/26, 7-9pm at the Peristyle in City Park

## Rep List

### Current Rep

{% for song in site.songs %}
{% if song.status == "current" %}
- [{{song.title}}]({{song.url}})
{% endif %}
{% endfor %}

### Songs we're currently learning
We have arrangements for these, and are working them up to play out.

{% for song in site.songs %}
{% if song.status == "learning" %}
- [{{song.title}}]({{song.url}})
{% endif %}
{% endfor %}

### Songs we want to play
We don't have arrangements for these yet, but they're on our radar.
If you want to make an arrangement that'd be cool.

{% for song in site.songs %}
{% if song.status == "future" %}
- [{{song.title}}]({{song.url}})
{% endif %}
{% endfor %}

