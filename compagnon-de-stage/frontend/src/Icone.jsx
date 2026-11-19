// Les petites icônes de l'application, dessinées en SVG (des traits, comme dans NomaUBL et Liberty Next).
// Chaque icône est une liste de formes : un texte = un tracé (« path »), un tableau = un cercle [cx, cy, r].

const DESSINS = {
  boussole: [[12, 12, 10], 'm16.24 7.76-2.12 6.36-6.36 2.12 2.12-6.36z'],
  calendrier: ['M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z', 'M16 2v4', 'M8 2v4', 'M3 10h18'],
  manette: ['M6 11h4', 'M8 9v4', 'M15 12h.01', 'M18 10h.01',
    'M17.32 5H6.68a4 4 0 0 0-3.98 3.59C2.6 9.42 2 14.46 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.41-1.41A2 2 0 0 1 9.83 16h4.34a2 2 0 0 1 1.42.59L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.54-.6-6.58-.7-7.41A4 4 0 0 0 17.32 5z'],
  carnet: ['M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z', 'M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z'],
  bug: ['m8 2 1.88 1.88', 'M14.12 3.88 16 2', 'M9 7.13v-1a3 3 0 1 1 6 0v1',
    'M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6', 'M12 20v-9', 'M6.53 9C4.6 8.8 3 7.1 3 5', 'M6 13H2',
    'M3 21c0-2.1 1.7-3.9 3.8-4', 'M20.97 5c0 2.1-1.6 3.8-3.5 4', 'M22 13h-4', 'M17.2 17c2.1.1 3.8 1.9 3.8 4'],
  lexique: ['M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20', 'M8 7h8', 'M8 11h6'],
  bouee: [[12, 12, 10], [12, 12, 4], 'm4.93 4.93 4.24 4.24', 'm14.83 9.17 4.24-4.24', 'm14.83 14.83 4.24 4.24', 'm9.17 14.83-4.24 4.24'],
  stagiaires: ['M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2', [9, 7, 4], 'M22 21v-2a4 4 0 0 0-3-3.87', 'M16 3.13a4 4 0 0 1 0 7.75'],
  documents: ['M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z', 'M14 2v4a2 2 0 0 0 2 2h4', 'M10 9H8', 'M16 13H8', 'M16 17H8'],
  reglages: ['M4 21v-7', 'M4 10V3', 'M12 21v-9', 'M12 8V3', 'M20 21v-5', 'M20 12V3', 'M2 14h4', 'M10 8h4', 'M18 16h4'],
  message: ['M7.9 20A9 9 0 1 0 4 16.1L2 22z'],
  soleil: [[12, 12, 4], 'M12 2v2', 'M12 20v2', 'm4.93 4.93 1.41 1.41', 'm17.66 17.66 1.41 1.41', 'M2 12h2', 'M20 12h2', 'm6.34 17.66-1.41 1.41', 'm19.07 4.93-1.41 1.41'],
  lune: ['M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z'],
  sortie: ['M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4', 'm16 17 5-5-5-5', 'M21 12H9'],
  jouer: [[12, 12, 10], 'm10 8 6 4-6 4z'],
  menu: ['M4 6h16', 'M4 12h16', 'M4 18h16'],
  fleche: ['M5 12h14', 'm12 5 7 7-7 7'],
  punaise: ['M12 17v5', 'M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z'],
}

export default function Icone({ nom, taille = 17 }) {
  const formes = DESSINS[nom]
  if (!formes) return null
  return (
    <svg className="icone" width={taille} height={taille} viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {formes.map((f, i) => (typeof f === 'string' ? <path key={i} d={f} /> : <circle key={i} cx={f[0]} cy={f[1]} r={f[2]} />))}
    </svg>
  )
}
