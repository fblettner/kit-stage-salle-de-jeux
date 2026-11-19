// La salle de jeux d'exemple, affichée dans le compagnon : les jeux sont un autre site (la solution de référence),
// qu'on montre ici dans un cadre (« iframe »), comme une fenêtre ouverte sur lui.
export default function Salle() {
  return <iframe className="salle" src="/jeux/" title="La salle de jeux" />
}
