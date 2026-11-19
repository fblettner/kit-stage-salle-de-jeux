import { useApi } from '../api.js'
import Blocs from '../Blocs.jsx'

// La page « Je suis bloqué » : le fichier autonomie/depannage.md du kit.
export default function Depannage({ ouvrirAide }) {
  const { donnees, erreur } = useApi('/depannage')
  if (erreur) return <p className="erreur">{erreur}</p>
  if (!donnees) return <p className="chargement">Chargement…</p>
  return (
    <div className="depannage">
      <article className="carte activite">
        <Blocs blocs={donnees} />
        <button className="lien-onglet" onClick={ouvrirAide}>🆘 Écrire à mon maître de stage →</button>
      </article>
    </div>
  )
}
