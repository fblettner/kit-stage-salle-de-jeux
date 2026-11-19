// Une carte de joueur, façon album de vignettes

const NOMS_COURTS = { G: 'GB', DEF: 'DEF', MIL: 'MIL', ATT: 'ATT' }

function couleurCarte(note) {
  if (note >= 80) return 'or'
  if (note >= 70) return 'argent'
  return 'bronze'
}

function initiales(nom) {
  return nom
    .split(' ')
    .map((mot) => mot[0])
    .join('')
    .slice(0, 2)
}

export default function CarteJoueur({ joueur, choisi, refus, onClick, petite }) {
  const stats = joueur.poste === 'G'
    ? [['ARR', joueur.defense], ['TEC', joueur.technique]]
    : [['ATT', joueur.attaque], ['DEF', joueur.defense], ['TEC', joueur.technique], ['VIT', joueur.vitesse]]

  return (
    <button
      type="button"
      className={`coach-carte coach-carte-${couleurCarte(joueur.note)} ${choisi ? 'choisi' : ''} ${petite ? 'petite' : ''}`}
      onClick={onClick}
      disabled={!onClick || (refus && !choisi)}
      title={refus ?? (choisi ? 'Cliquer pour retirer' : 'Cliquer pour recruter')}
    >
      <span className="coach-carte-haut">
        <span className="coach-carte-note">{joueur.note}</span>
        <span className="coach-carte-poste">{NOMS_COURTS[joueur.poste]}</span>
      </span>
      <span className="coach-carte-avatar">{initiales(joueur.nom)}</span>
      <span className="coach-carte-nom">{joueur.nom}</span>
      {!petite && (
        <span className="coach-carte-stats">
          {stats.map(([nom, valeur]) => (
            <span key={nom}><b>{valeur}</b> {nom}</span>
          ))}
        </span>
      )}
      {!petite && <span className="coach-carte-prix">{joueur.prix} M€</span>}
      {choisi && <span className="coach-carte-coche">✓</span>}
    </button>
  )
}
