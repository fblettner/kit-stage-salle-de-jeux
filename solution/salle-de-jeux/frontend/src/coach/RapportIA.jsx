// « Dans la tête de l'entraîneur adverse » : le résultat de ses simulations

export default function RapportIA({ decision, tactiques }) {
  if (!decision) return null
  const nomTactique = (id) => tactiques.find((t) => t.id === id)

  return (
    <div className="coach-rapport">
      <p className="coach-rapport-choix">
        Tactique choisie : <b>{nomTactique(decision.tactique)?.emoji} {nomTactique(decision.tactique)?.nom}</b>
      </p>
      {decision.rapport.length > 0 && (
        <>
          <div className="coach-legende">
            <span className="v">Victoire IA</span> <span className="n">Nul</span> <span className="d">Défaite IA</span>
          </div>
          {decision.rapport.map((ligne) => (
            <div key={ligne.tactique} className={`coach-rapport-ligne ${ligne.tactique === decision.tactique ? 'choisie' : ''}`}>
              <span className="coach-rapport-nom">{nomTactique(ligne.tactique)?.emoji} {ligne.nom}</span>
              <span className="coach-barre-empilee" title={`${ligne.victoire} % / ${ligne.nul} % / ${ligne.defaite} %`}>
                <span className="v" style={{ width: `${ligne.victoire}%` }}>{ligne.victoire >= 12 ? `${ligne.victoire}%` : ''}</span>
                <span className="n" style={{ width: `${ligne.nul}%` }} />
                <span className="d" style={{ width: `${ligne.defaite}%` }} />
              </span>
            </div>
          ))}
        </>
      )}
      <p className="discret">🧠 « {decision.explication} »</p>
    </div>
  )
}
