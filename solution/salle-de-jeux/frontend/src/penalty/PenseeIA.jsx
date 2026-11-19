// « Dans la tête de l'IA » : un petit but où chaque zone est colorée
// selon la probabilité que l'IA donnait à chaque zone.
const ZONES = ['haut-gauche', 'haut-centre', 'haut-droite', 'bas-gauche', 'bas-centre', 'bas-droite']

export default function PenseeIA({ pensee }) {
  if (!pensee) return <p className="discret">Joue un premier tir pour voir ce que pense l'IA.</p>

  return (
    <div>
      <p className="penalty-pensee-titre">{pensee.titre}</p>
      <div className="penalty-mini-but">
        {ZONES.map((zone) => {
          const probabilite = pensee.prediction[zone]
          return (
            <div key={zone} className="penalty-mini-zone" style={{ background: `rgba(234, 88, 12, ${Math.min(0.9, probabilite * 2)})` }}>
              {Math.round(probabilite * 100)} %
            </div>
          )
        })}
      </div>
      <p className="discret">🧠 « {pensee.explication} »</p>
    </div>
  )
}
