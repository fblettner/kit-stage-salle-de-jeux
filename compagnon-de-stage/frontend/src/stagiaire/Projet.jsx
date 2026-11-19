import { useState } from 'react'
import { api, useApi } from '../api.js'
import Markdown from '../Markdown.jsx'
import ZoneTexte from '../ZoneTexte.jsx'

export default function Projet({ moi, recharger, onRepondre, salle, allerA }) {
  const { donnees } = useApi('/catalogue')
  const [erreur, setErreur] = useState('')
  const [ouvert, setOuvert] = useState(null)

  async function choisir(jeu) {
    setErreur('')
    try {
      await api('/moi/jeu', { methode: 'PUT', corps: { jeu } })
      recharger()
    } catch (e) {
      setErreur(e.message)
    }
  }

  if (!donnees) return <p className="chargement">Chargement…</p>
  const memeJeu = moi.autres.filter((a) => a.jeu && a.jeu === moi.jeu)

  return (
    <div className="projet">
      <p className="discret">
        Joue d'abord aux jeux d'exemple, lis les fiches, puis choisis. Tu peux choisir le même jeu que l'autre stagiaire.
      </p>
      {moi.autres.some((a) => a.jeu) && (
        <p className="petit">
          {moi.autres.filter((a) => a.jeu).map((a) => `${a.prenom} a choisi : ${donnees.jeux.find((j) => j.jeu === a.jeu)?.nom}`).join(' · ')}
        </p>
      )}
      {salle && (
        <p>
          <button className="principal" onClick={() => allerA('salle')}>🎮 Jouer aux 4 jeux d'exemple →</button>
        </p>
      )}
      {erreur && <p className="erreur">{erreur}</p>}
      {moi.choix_verrouille && <p className="encart">🔒 Les choix sont validés par ton maître de stage.</p>}
      <div className="catalogue">
        {donnees.jeux.map((j) => {
          const choisi = moi.jeu === j.jeu
          return (
            <section key={j.jeu} className={`fiche-jeu carte ${choisi ? 'choisi' : ''}`}>
              <div className="fiche-icone">{j.icone}</div>
              <h3>{j.titre}</h3>
              <div className={`fiche-texte ${ouvert === j.jeu ? 'ouvert' : ''}`}>
                <Markdown texte={j.texte} />
              </div>
              <button className="discret-bouton" onClick={() => setOuvert(ouvert === j.jeu ? null : j.jeu)}>
                {ouvert === j.jeu ? 'Réduire ▲' : 'Lire toute la fiche ▼'}
              </button>
              <button className={choisi ? 'choisi-bouton' : 'principal'} disabled={choisi || moi.choix_verrouille} onClick={() => choisir(j.jeu)}>
                {choisi ? '✓ C\'est mon projet' : 'Je choisis ce jeu'}
              </button>
            </section>
          )
        })}
      </div>
      {memeJeu.length > 0 && (
        <div className="encart">
          <h3>Vous avez choisi le même jeu que {memeJeu.map((a) => a.prenom).join(', ')} !</h3>
          <p>
            Par défaut, vous serez deux « agences concurrentes » : chacun sa version, dans son dossier (le tien :{' '}
            <code>{moi.dossier}</code>). Ton maître de stage peut aussi choisir la formule « une équipe, deux métiers ».
          </p>
          <details>
            <summary>Lire les deux formules</summary>
            <Markdown texte={donnees.meme_jeu} />
          </details>
        </div>
      )}
      {moi.jeu && (
        <div className="carte">
          <h3>Pourquoi j'ai choisi ce jeu</h3>
          <ZoneTexte cle="0-pourquoi" valeur={moi.reponses['0-pourquoi'] || ''} onRepondre={onRepondre}
            placeholder="Parce que…" />
        </div>
      )}
    </div>
  )
}
