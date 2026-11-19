// Une barre horizontale pour une note sur 100
export default function Jauge({ nom, valeur }) {
  return (
    <div className="coach-jauge">
      <span>{nom}</span>
      <span className="coach-jauge-fond"><span style={{ width: `${valeur}%` }} /></span>
      <b>{valeur}</b>
    </div>
  )
}
