// L'affichage du match en direct : tableau d'affichage, terrain, commentaires

// Qui domine en ce moment ? (la possession sur les 8 dernières minutes, de -1 à +1)
function domination(possession, minute) {
  const recentes = possession.slice(Math.max(0, minute - 8), minute)
  if (recentes.length === 0) return 0
  return recentes.reduce((s, c) => s + (c === 'joueur' ? 1 : -1), 0) / recentes.length
}

export default function Match({ nomClub, nomIA, evenements, possession, minute }) {
  const visibles = evenements.filter((e) => e.minute <= minute)
  const butsJoueur = visibles.filter((e) => e.type === 'but' && e.equipe === 'joueur').length
  const butsIA = visibles.filter((e) => e.type === 'but' && e.equipe === 'ia').length
  const dom = domination(possession, minute)

  return (
    <div className="coach-match">
      <div className="coach-tableau">
        <span className="coach-tableau-club">{nomClub}</span>
        <span className="coach-tableau-score">{butsJoueur} - {butsIA}</span>
        <span className="coach-tableau-club ia">{nomIA}</span>
      </div>
      <div className="coach-chrono">
        <span style={{ width: `${(100 * minute) / 90}%` }} />
        <b>{minute}'</b>
      </div>

      {/* Le ballon se déplace vers le but de l'équipe qui domine */}
      <div className="coach-pelouse">
        <span className="coach-ligne-mediane" />
        <span className="coach-rond-central" />
        <span className="coach-cage gauche" />
        <span className="coach-cage droite" />
        <span className="coach-ballon" style={{ left: `${50 + dom * 38}%` }}>⚽</span>
        <span className="coach-pelouse-nom gauche">{nomClub}</span>
        <span className="coach-pelouse-nom droite">{nomIA}</span>
      </div>

      <ol className="coach-commentaires" aria-live="polite">
        {[...visibles].reverse().map((e, i) => (
          <li key={`${e.minute}-${i}-${e.type}`} className={`coach-evenement ${e.type} ${e.equipe ?? ''}`}>
            <span className="coach-evenement-minute">{e.minute}'</span>
            <span>{e.texte}</span>
          </li>
        ))}
      </ol>
    </div>
  )
}
