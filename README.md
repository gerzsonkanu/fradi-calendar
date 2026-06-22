# Ferencváros NB I Naptár 🟢

Automatikusan frissülő Apple Calendar az OTP Bank Liga Ferencváros mérkőzéseivel.

## Feliratkozás

Másold be ezt a linkt az Apple Calendarba (File → New Calendar Subscription):

```
webcal://GITHUB_FELHASZNÁLÓNÉV.github.io/fradi-calendar/ferencvaros.ics
```

## Hogyan működik?

- Minden hétfőn reggel a GitHub Actions lekéri az MLSZ adatbank oldalát
- Generál egy friss `.ics` fájlt
- Az Apple Calendar automatikusan frissül
