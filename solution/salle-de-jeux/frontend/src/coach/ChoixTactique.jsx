// Les boutons pour choisir sa tactique
export default function ChoixTactique({ tactiques, valeur, onChange }) {
  return (
    <div className="coach-tactiques">
      {tactiques.map((t) => (
        <button
          key={t.id}
          type="button"
          className={`coach-tactique ${valeur === t.id ? 'choisie' : ''}`}
          onClick={() => onChange(t.id)}
        >
          <span className="coach-tactique-titre">{t.emoji} {t.nom}</span>
          <span className="coach-tactique-description">{t.description}</span>
        </button>
      ))}
    </div>
  )
}
