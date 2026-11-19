import { useEffect, useState } from 'react'
import { useApi } from '../api.js'
import ZoneTexte from '../ZoneTexte.jsx'

// Le carnet de bord : les questions viennent du fichier fiches/carnet-de-bord.md.
export default function Carnet({ moi, prenom, jeu, onRepondre, lectureSeule: lectureDemandee = false }) {
  const { donnees } = useApi('/carnet/questions')
  // Pour imprimer, on affiche les réponses en texte (les zones de saisie s'impriment mal)
  const [impression, setImpression] = useState(false)
  const lectureSeule = lectureDemandee || impression
  useEffect(() => {
    if (!impression) return
    const fin = () => setImpression(false)
    window.addEventListener('afterprint', fin)
    const id = setTimeout(() => window.print(), 50)
    return () => {
      clearTimeout(id)
      window.removeEventListener('afterprint', fin)
    }
  }, [impression])
  if (!donnees) return <p className="chargement">Chargement…</p>

  return (
    <div className="carnet">
      <div className="carnet-entete">
        <div>
          <h2>Carnet de bord de {prenom}</h2>
        </div>
        {!lectureDemandee && (
          <button className="secondaire pas-imprime" onClick={() => setImpression(true)}>🖨️ Imprimer</button>
        )}
      </div>
      <p>
        <strong>Mon jeu :</strong> {jeu ? `${jeu.icone} ${jeu.nom}` : '—'}
        {moi.reponses['0-pourquoi'] && (
          <>
            <br />
            <strong>Pourquoi j'ai choisi ce jeu :</strong> {moi.reponses['0-pourquoi']}
          </>
        )}
      </p>
      {donnees.map((jour, n) => (
        <section key={jour.titre} className="carnet-jour carte">
          <h3>{jour.titre}</h3>
          {jour.questions.map((q) => (
            <Question key={q.cle} q={q} moi={moi} onRepondre={onRepondre} lectureSeule={lectureSeule} />
          ))}
          {/* Le bilan du jour, écrit à la fin de la dernière activité (lundi = bilan-0 … vendredi = bilan-4) */}
          {n < 5 && moi.reponses[`bilan-${n}`] && (
            <div className="question">
              <p className="question-titre">Mon bilan du jour</p>
              <p className="reponse-lue">{moi.reponses[`bilan-${n}`]}</p>
            </div>
          )}
        </section>
      ))}
    </div>
  )
}

function Question({ q, moi, onRepondre, lectureSeule }) {
  const valeur = (cle) => moi.reponses[cle] || ''
  if (lectureSeule) {
    if (q.type === 'tableau') {
      return (
        <div className="question">
          <p className="question-titre">{q.titre}</p>
          <Tableau q={q} rendu={(cle) => valeur(cle) || <span className="discret">—</span>} />
        </div>
      )
    }
    return (
      <div className="question">
        <p className="question-titre">{q.titre}</p>
        <p className="reponse-lue">{valeur(q.cle) || <span className="discret">(pas encore de réponse)</span>}</p>
      </div>
    )
  }
  return (
    <div className="question">
      <p className="question-titre">{q.titre}</p>
      {q.type === 'schema' && (
        <p className="discret petit">✏️ Dessine-le sur papier ; ici, écris ce qu'il y a sur ton schéma (les blocs et les flèches).</p>
      )}
      {q.type === 'tableau' ? (
        <Tableau
          q={q}
          rendu={(cle) => <ZoneTexte cle={cle} valeur={valeur(cle)} onRepondre={onRepondre} lignes={2} />}
        />
      ) : q.type === 'ligne' ? (
        <ZoneTexte cle={q.cle} valeur={valeur(q.cle)} onRepondre={onRepondre} uneLigne prefixe={q.prefixe} />
      ) : (
        <ZoneTexte cle={q.cle} valeur={valeur(q.cle)} onRepondre={onRepondre} lignes={q.type === 'schema' ? 4 : 3} />
      )}
    </div>
  )
}

function Tableau({ q, rendu }) {
  // La 1re colonne contient l'intitulé de la ligne (Facile, Moyen…) quand il existe ; sinon toutes les colonnes se remplissent.
  const avecIntitules = q.lignes.some((l) => l)
  const colonnes = avecIntitules ? q.colonnes.slice(1) : q.colonnes
  return (
    <div className="tableau-carnet">
      <table>
        <thead>
          <tr>
            {avecIntitules && <th>{q.colonnes[0]}</th>}
            {colonnes.map((c) => <th key={c}>{c}</th>)}
          </tr>
        </thead>
        <tbody>
          {q.lignes.map((l, r) => (
            <tr key={r}>
              {avecIntitules && <th>{l}</th>}
              {colonnes.map((_, c) => <td key={c}>{rendu(`${q.cle}:${r}:${c}`)}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
