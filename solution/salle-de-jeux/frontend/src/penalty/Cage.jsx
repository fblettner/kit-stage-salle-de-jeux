// Le dessin du but : le filet, le gardien, le ballon et le viseur.
// Les positions sont des points du but : x de 0 (poteau gauche) à 1 (poteau droit), y de 0 (barre) à 1 (sol).
import { useRef } from 'react'

// Un petit gardien dessiné en SVG (on peut changer la couleur du maillot)
function Gardien({ couleur }) {
  return (
    <svg viewBox="0 0 60 70" aria-hidden="true">
      <line x1="18" y1="26" x2="5" y2="9" stroke={couleur} strokeWidth="7" strokeLinecap="round" />
      <line x1="42" y1="26" x2="55" y2="9" stroke={couleur} strokeWidth="7" strokeLinecap="round" />
      <circle cx="5" cy="8" r="5.5" fill="#fff" />
      <circle cx="55" cy="8" r="5.5" fill="#fff" />
      <line x1="25" y1="46" x2="21" y2="66" stroke="#222" strokeWidth="7" strokeLinecap="round" />
      <line x1="35" y1="46" x2="39" y2="66" stroke="#222" strokeWidth="7" strokeLinecap="round" />
      <rect x="17" y="20" width="26" height="28" rx="7" fill={couleur} />
      <circle cx="30" cy="11" r="8" fill="#f1c27d" />
    </svg>
  )
}

const POSITION_GARDIEN = { x: 0.5, y: 0.62 } // debout au milieu
const POINT_PENALTY = { x: 0.5, y: 1.55 }

export default function Cage({ viseur, balle, gardien, couleurGardien, interactif, onSurvol, onClic }) {
  const refBut = useRef(null)

  // Convertit la position de la souris (ou du doigt) en point du but
  function pointDepuis(evenement) {
    const rect = refBut.current.getBoundingClientRect()
    const borner = (v) => Math.min(1, Math.max(0, v))
    return {
      x: borner((evenement.clientX - rect.left) / rect.width),
      y: borner((evenement.clientY - rect.top) / rect.height),
    }
  }

  const g = gardien ?? POSITION_GARDIEN
  const rotation = gardien ? Math.max(-65, Math.min(65, (gardien.x - 0.5) * 140)) : 0
  const b = balle ?? POINT_PENALTY

  return (
    <div className="penalty-terrain">
      <div
        ref={refBut}
        className={`penalty-but ${interactif ? 'interactif' : ''}`}
        onPointerMove={(e) => interactif && onSurvol?.(pointDepuis(e))}
        onClick={(e) => interactif && onClic?.(pointDepuis(e))}
      >
        <div
          className="penalty-gardien"
          style={{ left: `${g.x * 100}%`, top: `${g.y * 100}%`, transform: `translate(-50%, -50%) rotate(${rotation}deg)` }}
        >
          <Gardien couleur={couleurGardien} />
        </div>
        {viseur && (
          <span className="penalty-viseur" style={{ left: `${viseur.x * 100}%`, top: `${viseur.y * 100}%` }} />
        )}
        <span className="penalty-point" style={{ left: '50%', top: `${POINT_PENALTY.y * 100}%` }} />
        <span
          className={`penalty-balle ${balle ? 'en-vol' : 'repos'}`}
          style={{ left: `${b.x * 100}%`, top: `${b.y * 100}%` }}
        >
          ⚽
        </span>
      </div>
    </div>
  )
}
