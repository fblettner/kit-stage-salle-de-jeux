import { useState } from 'react'
import { api } from '../api.js'
import { trouverActivite } from '../Semaine.jsx'

// La demande d'aide : on encourage d'abord à chercher (le message d'erreur, Claude), comme un vrai développeur.
export default function Aide({ moi, programme, activite, recharger, onFermer, allerA }) {
  const [message, setMessage] = useState('')
  const [cases, setCases] = useState({ relu: false, claude: false })
  const [erreur, setErreur] = useState('')
  const [envoye, setEnvoye] = useState(false)
  const act = trouverActivite(programme, activite)

  async function envoyer(e) {
    e.preventDefault()
    setErreur('')
    try {
      await api('/moi/aides', { methode: 'POST', corps: { activite: act ? act.id : 'autre', message } })
      setMessage('')
      setEnvoye(true)
      recharger()
    } catch (err) {
      setErreur(err.message)
    }
  }

  async function resolue(id) {
    await api(`/moi/aides/${id}/resolue`, { methode: 'POST' })
    recharger()
  }

  const enCours = moi.aides.filter((a) => a.statut !== 'resolue')

  return (
    <div className="fond-modale" onClick={onFermer}>
      <div className="modale" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Demander de l'aide">
        <div className="modale-entete">
          <h2>J'ai besoin d'aide</h2>
          <button className="discret-bouton carre" onClick={onFermer} aria-label="Fermer">✕</button>
        </div>

        {enCours.length > 0 && (
          <div className="mes-aides">
            {enCours.map((a) => (
              <div key={a.id} className={`aide-item ${a.statut}`}>
                <p className="petit discret">Ma question :</p>
                <p>{a.message}</p>
                {a.reponse ? (
                  <p className="reponse-tuteur">💬 <strong>Réponse :</strong> {a.reponse}</p>
                ) : (
                  <p className="discret petit">⏳ Ton maître de stage a reçu ta demande, il arrive dès que possible.</p>
                )}
                <button className="secondaire petit-bouton" onClick={() => resolue(a.id)}>✓ C'est réglé, merci</button>
              </div>
            ))}
          </div>
        )}

        {envoye ? (
          <div className="encart">
            <p>
              ✅ Demande envoyée ! En attendant, ne reste pas bloqué : passe à une autre partie, teste le jeu de l'autre stagiaire,
              ou remplis ton carnet de bord.
            </p>
            <button className="secondaire" onClick={() => setEnvoye(false)}>Poser une autre question</button>
          </div>
        ) : (
          <form onSubmit={envoyer}>
            <p className="petit">Un vrai développeur, avant d'appeler un collègue :</p>
            <label className="case">
              <input type="checkbox" checked={cases.relu} onChange={(e) => setCases({ ...cases, relu: e.target.checked })} />
              J'ai relu le message d'erreur (dans le terminal ou la console du navigateur, touche F12)
            </label>
            <label className="case">
              <input type="checkbox" checked={cases.claude} onChange={(e) => setCases({ ...cases, claude: e.target.checked })} />
              J'ai demandé à Claude, en lui collant l'erreur et en expliquant ce que j'attendais
            </label>
            <label className="case">
              <input type="checkbox" checked={!!cases.autre} onChange={(e) => setCases({ ...cases, autre: e.target.checked })} />
              J'ai regardé la page <button type="button" className="lien" onClick={() => allerA('depannage')}>« Je suis bloqué »</button>
            </label>
            <label>
              Mon problème {act && <span className="discret">(activité : {act.titre})</span>}
              <textarea rows={3} value={message} onChange={(e) => setMessage(e.target.value)}
                placeholder="Ce que j'essaie de faire, ce qui se passe à la place, ce que j'ai déjà essayé…" maxLength={1000} />
            </label>
            {erreur && <p className="erreur">{erreur}</p>}
            <button className="principal large" disabled={message.trim().length < 3}>Appeler mon maître de stage</button>
            {!(cases.relu && cases.claude && cases.autre) && message.trim().length >= 3 && (
              <p className="discret petit">Tu peux envoyer quand même, mais essaie d'abord les trois cases : souvent, ça suffit !</p>
            )}
          </form>
        )}
      </div>
    </div>
  )
}
