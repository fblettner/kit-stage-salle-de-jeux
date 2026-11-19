import { useEffect, useState } from 'react'
import { lienSalle, useApi } from '../api.js'
import Salle from '../Salle.jsx'
import Coquille from '../Coquille.jsx'
import Aides from './Aides.jsx'
import Documents from './Documents.jsx'
import Journee from './Journee.jsx'
import Reglages from './Reglages.jsx'
import Stagiaires from './Stagiaires.jsx'

export default function Animateur({ onDeconnexion }) {
  const [onglet, setOnglet] = useState('journee')
  const programme = useApi('/programme', { toutesLes: 60 })
  const tableau = useApi('/animateur/tableau', { toutesLes: 10 })

  const aides = tableau.donnees?.aides_ouvertes ?? 0
  useEffect(() => {
    document.title = aides ? `(${aides}) 🆘 Compagnon de stage` : 'Compagnon de stage'
  }, [aides])

  if (!programme.donnees || !tableau.donnees)
    return <p className="chargement">{programme.erreur || tableau.erreur || 'Chargement…'}</p>

  const sections = [
    {
      titre: 'Pilotage',
      liens: [
        { cle: 'journee', nom: 'Le programme', icone: 'calendrier', description: 'Heure par heure : tes fiches, et où en est chaque stagiaire' },
        { cle: 'stagiaires', nom: 'Stagiaires', icone: 'stagiaires', description: 'Les comptes, les codes, les carnets de bord' },
        { cle: 'aides', nom: 'Aides', icone: 'message', badge: aides, titre: "Les demandes d'aide", description: 'Réponds par écrit (le stagiaire voit ta réponse sur son écran), ou vas-y' },
      ],
    },
    {
      titre: 'Le kit',
      liens: [
        { cle: 'documents', nom: 'Documents', icone: 'documents', description: 'Tous les fichiers du kit, et le CLAUDE.md déjà rempli' },
        { cle: 'reglages', nom: 'Réglages', icone: 'reglages', description: 'Le calendrier, ce que voient les stagiaires, la fin du stage' },
      ],
    },
  ]
  const salle = lienSalle(programme.donnees)
  if (salle) sections[1].liens.unshift(salle)
  const recharger = () => {
    tableau.recharger()
    programme.recharger()
  }

  return (
    <Coquille
      sections={sections}
      page={onglet}
      allerA={setOnglet}
      onDeconnexion={onDeconnexion}
      qui={
        <>
          <strong>Maître de stage</strong>
          <span>{tableau.donnees.stagiaires.length} stagiaire{tableau.donnees.stagiaires.length > 1 ? 's' : ''}</span>
        </>
      }
      actions={
        <>
          {aides > 0 && (
            <button className="bouton-aide" onClick={() => setOnglet('aides')}>
              {aides} demande{aides > 1 ? 's' : ''}
            </button>
          )}
        </>
      }
    >
      {onglet === 'journee' && <Journee programme={programme.donnees} tableau={tableau.donnees} recharger={recharger} allerA={setOnglet} />}
      {onglet === 'stagiaires' && <Stagiaires programme={programme.donnees} tableau={tableau.donnees} recharger={recharger} />}
      {onglet === 'aides' && <Aides programme={programme.donnees} recharger={recharger} />}
      {onglet === 'salle' && <Salle />}
      {onglet === 'documents' && <Documents />}
      {onglet === 'reglages' && <Reglages programme={programme.donnees} tableau={tableau.donnees} recharger={recharger} />}
    </Coquille>
  )
}
