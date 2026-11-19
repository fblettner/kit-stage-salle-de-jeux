// Les onglets des 5 jours et la frise des activités d'un jour (utilisés par l'animateur et les stagiaires).

export function OngletsJours({ programme, jour, setJour }) {
  return (
    <div className="jours">
      {programme.jours.map((j) => (
        <button
          key={j.index}
          className={`${jour === j.index ? 'actif' : ''} ${programme.jour_actuel === j.index ? 'aujourdhui' : ''}`}
          onClick={() => setJour(j.index)}
        >
          {j.nom}
          {programme.jour_actuel === j.index && <span className="point" title="Aujourd'hui" />}
        </button>
      ))}
    </div>
  )
}

export function Frise({ programme, jour, choisie, onChoisir, badge }) {
  const j = programme.jours[jour]
  return (
    <ol className="frise">
      {j.activites.map((a, i) => {
        const avantMidi = i > 0 && j.activites[i - 1].fin <= '12:00' && a.debut >= '13:00'
        return (
          <li key={a.id}>
            {avantMidi && <div className="midi">🍽️ Pause déjeuner</div>}
            <button
              className={`etape ${choisie === a.id ? 'choisie' : ''} ${programme.activite_actuelle === a.id ? 'en-cours' : ''}`}
              onClick={() => onChoisir(a.id)}
            >
              <span className="heure">{a.debut}</span>
              <span className="etape-titre">
                {a.titre}
                <span className={`mode mode-${a.mode}`}>{a.mode === 'perso' ? 'Mon jeu' : 'Ensemble'}</span>
                {programme.activite_actuelle === a.id && <span className="maintenant">maintenant</span>}
              </span>
              {badge && <span className="etape-badge">{badge(a)}</span>}
            </button>
          </li>
        )
      })}
    </ol>
  )
}

export function trouverActivite(programme, id) {
  for (const j of programme.jours) {
    const a = j.activites.find((x) => x.id === id)
    if (a) return a
  }
  return null
}
