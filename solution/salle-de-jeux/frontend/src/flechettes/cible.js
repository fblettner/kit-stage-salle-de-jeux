// Les dimensions officielles d'une cible de fléchettes (en mm, depuis le centre)
// et de quoi la dessiner. (Le calcul des points, lui, est fait par le serveur : c'est l'arbitre.)

export const RAYON_BULL = 6.35
export const RAYON_BULL_25 = 15.9
export const TRIPLE = [99, 107]
export const DOUBLE = [162, 170]
export const RAYON_CIBLE = DOUBLE[1]

// Les 20 secteurs, dans le sens des aiguilles d'une montre, en partant du haut
export const SECTEURS = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

// Un point (rayon, angle depuis le haut dans le sens des aiguilles d'une montre) → coordonnées du dessin SVG
// (dans un SVG, l'axe y va vers le BAS, d'où le signe moins)
export function polaire(rayon, angleDegres) {
  const a = (angleDegres * Math.PI) / 180
  return [rayon * Math.sin(a), -rayon * Math.cos(a)]
}

// Le chemin SVG d'un morceau d'anneau entre deux rayons et deux angles
export function morceauAnneau(r1, r2, a1, a2) {
  const [x1, y1] = polaire(r2, a1)
  const [x2, y2] = polaire(r2, a2)
  const [x3, y3] = polaire(r1, a2)
  const [x4, y4] = polaire(r1, a1)
  return `M ${x1} ${y1} A ${r2} ${r2} 0 0 1 ${x2} ${y2} L ${x3} ${y3} A ${r1} ${r1} 0 0 0 ${x4} ${y4} Z`
}

// Le serveur parle en mm avec y vers le HAUT ; le dessin SVG a y vers le BAS
export const versSvg = (p) => ({ x: p.x, y: -p.y })
