// Le dessin de la cible, avec le viseur, les fléchettes plantées et (si on veut) la carte de chaleur.
// Positions en mm depuis le centre, y vers le haut (comme le serveur).
import { memo, useRef } from 'react'
import { DOUBLE, RAYON_BULL, RAYON_BULL_25, RAYON_CIBLE, SECTEURS, TRIPLE, morceauAnneau, polaire, versSvg } from './cible.js'

const TAILLE = 460 // le dessin va de -230 à +230 mm

// La cible elle-même ne change jamais : on la dessine une seule fois (memo)
const DessinCible = memo(function DessinCible() {
  return (
    <g>
      <circle r={225} fill="#1d1d1b" />
      {SECTEURS.map((numero, i) => {
        const a1 = -9 + 18 * i
        const a2 = a1 + 18
        const sombre = i % 2 === 0
        const simple = sombre ? '#1d1d1b' : '#f3e7c9'
        const anneau = sombre ? '#d0312d' : '#1a7f3b'
        const [tx, ty] = polaire(196, a1 + 9)
        return (
          <g key={numero}>
            <path d={morceauAnneau(RAYON_BULL_25, TRIPLE[0], a1, a2)} fill={simple} />
            <path d={morceauAnneau(TRIPLE[0], TRIPLE[1], a1, a2)} fill={anneau} />
            <path d={morceauAnneau(TRIPLE[1], DOUBLE[0], a1, a2)} fill={simple} />
            <path d={morceauAnneau(DOUBLE[0], DOUBLE[1], a1, a2)} fill={anneau} />
            <text x={tx} y={ty} className="flechettes-numero">{numero}</text>
          </g>
        )
      })}
      <circle r={RAYON_BULL_25} fill="#1a7f3b" />
      <circle r={RAYON_BULL} fill="#d0312d" />
      <circle r={RAYON_CIBLE} fill="none" stroke="#c9c9c9" strokeWidth="1" />
    </g>
  )
})

// La carte de chaleur : on montre seulement les meilleurs endroits, du jaune (bien) au rouge (le meilleur)
function CarteDeChaleur({ carte }) {
  const gains = carte.map((c) => c.gain)
  const min = Math.min(...gains)
  const max = Math.max(...gains)
  return (
    <g pointerEvents="none">
      {carte.map((c) => {
        const t = max > min ? (c.gain - min) / (max - min) : 0
        if (t < 0.65) return null // les endroits moyens ou mauvais restent transparents
        const force = (t - 0.65) / 0.35 // de 0 (bien) à 1 (le meilleur)
        const p = versSvg(c)
        return <circle key={`${c.x},${c.y}`} cx={p.x} cy={p.y} r={7}
          fill={`hsl(${55 - 55 * force}, 100%, 52%)`} opacity={0.65 + 0.3 * force} stroke="#fff" strokeWidth={0.8} />
      })}
    </g>
  )
}

function Flechette({ point, couleur }) {
  const p = versSvg(point)
  return (
    <g pointerEvents="none">
      <line x1={p.x} y1={p.y} x2={p.x + 16} y2={p.y - 16} stroke="#333" strokeWidth="3" />
      <path d={`M ${p.x + 14} ${p.y - 14} l 10 -2 l -6 -6 z`} fill={couleur} />
      <circle cx={p.x} cy={p.y} r="4.5" fill={couleur} stroke="#fff" strokeWidth="1.5" />
    </g>
  )
}

export default function Cible({ flechettes, viseur, viseeIA, conseil, carte, interactif, onSurvol, onSortie, onClic }) {
  const refSvg = useRef(null)

  // Position de la souris → point de la cible en mm (y vers le haut)
  function pointDepuis(evenement) {
    const rect = refSvg.current.getBoundingClientRect()
    return {
      x: ((evenement.clientX - rect.left) / rect.width) * TAILLE - TAILLE / 2,
      y: -(((evenement.clientY - rect.top) / rect.height) * TAILLE - TAILLE / 2),
    }
  }

  const v = viseur && versSvg(viseur)
  const vi = viseeIA && versSvg(viseeIA)
  const c = conseil && versSvg(conseil)

  return (
    <svg
      ref={refSvg}
      className={`flechettes-cible ${interactif ? 'interactif' : ''}`}
      viewBox={`${-TAILLE / 2} ${-TAILLE / 2} ${TAILLE} ${TAILLE}`}
      onPointerMove={(e) => interactif && onSurvol?.(pointDepuis(e))}
      onPointerLeave={() => onSortie?.()}
      onClick={(e) => interactif && onClic?.(pointDepuis(e))}
    >
      <DessinCible />
      {carte && <CarteDeChaleur carte={carte} />}
      {c && <circle cx={c.x} cy={c.y} r="14" className="flechettes-conseil" />}
      {vi && <circle cx={vi.x} cy={vi.y} r="12" className="flechettes-visee-ia" />}
      {flechettes.map((f, i) => <Flechette key={i} point={f.impact} couleur={f.couleur} />)}
      {v && (
        <g pointerEvents="none" className="flechettes-viseur">
          <circle cx={v.x} cy={v.y} r="9" />
          <line x1={v.x - 15} y1={v.y} x2={v.x + 15} y2={v.y} />
          <line x1={v.x} y1={v.y - 15} x2={v.x} y2={v.y + 15} />
        </g>
      )}
    </svg>
  )
}
