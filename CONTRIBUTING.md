# Come contribuire

Grazie per l'interesse verso questo progetto. Queste indicazioni servono a rendere i contributi
prevedibili e veloci da revisionare.

## Preparare l'ambiente

```bash
git clone https://github.com/LorenzoVenuti/license-plate-recognition.git
cd license-plate-recognition
# comandi di setup dell'ambiente di sviluppo
```

## Proporre una modifica

1. Apri un branch dal `main`: `git checkout -b feature-<nome-funzionalità>`.
2. Fai commit piccoli e nominabili, messaggi in inglese all'imperativo presente
   (`Add CSV export`, `Fix crash on empty input`).
3. Assicurati che i test passino.
4. Apri una pull request spiegando **cosa cambia e perché**.

## Segnalare un problema

Apri una issue usando il template: servono i passi per riprodurre il problema, il comportamento
atteso, quello osservato, e versione/sistema operativo.

## Standard

- Nessun segreto, chiave o dato personale nel codice o nei test.
- La documentazione va aggiornata insieme al codice: un README che descrive funzionalità che non
  esistono più è peggio di nessun README.
- Le modifiche che cambiano il comportamento pubblico vanno annotate in `CHANGELOG.md`.

## Sicurezza

Le vulnerabilità **non** vanno segnalate con una issue pubblica: vedi [SECURITY.md](SECURITY.md).
