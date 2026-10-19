#!/usr/bin/env python3
"""Pages locales (SEO local) : une page par ville ou pôle d'activité, plus la page
/zones-intervention qui les regroupe.

Pour ajouter une ville : ajoutez une entrée dans VILLES (contenu local propre à la
ville, pas un simple changement de nom), puis lancez
    python3 scripts/pages.py --sitemap && python3 scripts/blog.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages  # noqa: E402
from pages import esc, hero, cta_row, faq, final, write, TICK  # noqa: E402

# Chaque entrée : contenu propre à la zone. Les faits cités sont volontairement
# généraux (types de sites, contraintes connues) : aucun chiffre inventé.
VILLES = [
    # ------------------------------------------------------------------ VILLES
    dict(
        slug='lyon', groupe='ville', nom='Lyon', a='à Lyon', dept='Rhône (69)', cp='69007',
        title="Ombrière Solaire Lyon : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Lyon et dans la Métropole : loi APER, échéances, financement. Étude gratuite par un installateur de la région.",
        h1="Ombrières solaires de parking <em>à Lyon et dans la Métropole</em>",
        sub="Commerces de périphérie, sièges d'entreprises, hôpitaux, campus : les grands parkings extérieurs de la Métropole de Lyon sont concernés par la loi APER. Un installateur de la région étudie votre site gratuitement.",
        points=["Parkings extérieurs de la Métropole de Lyon", "Prise en compte du PLU-H et des secteurs protégés", "Installateur intervenant dans le Rhône"],
        contexte="""<h2>Quels parkings sont concernés à Lyon ?</h2>
<p>Au cœur de Lyon, une grande partie du stationnement est souterraine ou en ouvrage : ces parkings ne relèvent pas de l'obligation d'ombrières, qui vise les <strong>parcs extérieurs de plus de 1 500 m²</strong>. Les sites concernés se trouvent surtout en périphérie et dans les communes de la Métropole : zones commerciales, parcs d'activités, établissements de santé, campus universitaires, parkings relais et équipements sportifs.</p>""",
        sites=["Les <strong>zones commerciales de périphérie</strong> de l'est et du nord de l'agglomération, aux parkings clients très étendus.",
               "Les <strong>parcs tertiaires et sièges sociaux</strong> de Gerland, de Vaise ou de l'est lyonnais, avec des parkings salariés en surface.",
               "Les <strong>hôpitaux et cliniques</strong>, dont les parkings visiteurs et personnels fonctionnent jour et nuit.",
               "Les <strong>campus</strong> de Villeurbanne, Bron ou Écully, et les <strong>parkings relais</strong> en bout de ligne de transport."],
        local="""<h2>Ce qui change pour un projet dans la Métropole</h2>
<ul>
<li><strong>Urbanisme :</strong> le PLU-H de la Métropole fixe des règles d'aspect, de hauteur et de végétalisation à vérifier dès l'esquisse.</li>
<li><strong>Secteurs patrimoniaux :</strong> à proximité du site historique classé à l'UNESCO ou de monuments protégés, l'avis de l'architecte des Bâtiments de France peut être requis.</li>
<li><strong>Ombrage végétal :</strong> la Métropole mène une politique active de végétalisation. Combiner arbres et ombrières, désormais possible dans certaines limites, peut faciliter l'insertion du projet.</li>
<li><strong>Consommation sur place :</strong> bureaux, commerces et hôpitaux consomment en journée, un bon profil pour l'autoconsommation.</li>
</ul>""",
        faq=[("Mon parking souterrain à Lyon est-il concerné ?", "Non. L'obligation d'ombrières de la loi APER vise les parcs de stationnement extérieurs. Si votre site combine un niveau souterrain et une partie en surface, seule la partie extérieure est prise en compte."),
             ("Faut-il un permis pour une ombrière dans la Métropole ?", "Une autorisation d'urbanisme est en général nécessaire, déclaration préalable ou permis selon la taille du projet. Le dossier doit respecter le PLU-H et, en secteur protégé, recueillir l'avis de l'architecte des Bâtiments de France."),
             ("Intervenez-vous dans toutes les communes de la Métropole ?", "Oui : Villeurbanne, Vénissieux, Vaulx-en-Velin, Bron, Saint-Priest, Écully, Rillieux-la-Pape et les autres communes de la Métropole. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['saint-priest', 'limonest', 'villefranche-sur-saone', 'vienne', 'saint-quentin-fallavier', 'plaine-de-l-ain'],
    ),
    dict(
        slug='saint-etienne', groupe='ville', nom='Saint-Étienne', a='à Saint-Étienne', dept='Loire (42)', cp='42000',
        title="Ombrière Solaire Saint-Étienne : Parkings, Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Saint-Étienne et dans la Loire : zones commerciales, sites industriels, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Saint-Étienne et dans la Loire</em>",
        sub="Zones commerciales, sites industriels et logistiques, établissements de santé : dans l'agglomération stéphanoise et la plaine du Forez, de nombreux parkings dépassent le seuil de la loi APER.",
        points=["Saint-Étienne Métropole et plaine du Forez", "Sites industriels et logistiques", "Installateur intervenant dans la Loire"],
        contexte="""<h2>Les parkings concernés autour de Saint-Étienne</h2>
<p>Le tissu économique stéphanois, à la fois industriel, commercial et logistique, compte de nombreux parcs de stationnement extérieurs de plus de 1 500 m². Les plus grands, au-delà de 10 000 m², relèvent de l'échéance la plus proche.</p>""",
        sites=["Les <strong>zones commerciales</strong> de l'agglomération, notamment dans le secteur de Monthieu et du Pont-de-l'Âne.",
               "Les <strong>sites industriels</strong> de la vallée du Gier et de l'Ondaine, aux parkings salariés étendus.",
               "Les <strong>parcs d'activités de la plaine du Forez</strong>, autour d'Andrézieux-Bouthéon, avec des plateformes logistiques.",
               "Les <strong>établissements de santé et campus</strong> de l'agglomération."],
        local="""<h2>Les points à anticiper dans la Loire</h2>
<ul>
<li><strong>Relief :</strong> beaucoup de parkings sont en pente ou en terrasses. La structure et les fondations doivent s'adapter au terrain, ce qui se vérifie lors de la visite.</li>
<li><strong>Climat :</strong> les hivers peuvent être enneigés sur les hauteurs de l'agglomération. Les charges de neige sont intégrées au dimensionnement de la structure.</li>
<li><strong>Sites industriels :</strong> certains sont classés ICPE, avec des règles de distance qui peuvent modifier la surface concernée.</li>
<li><strong>Autoconsommation :</strong> ateliers et entrepôts consomment en journée, au moment où les ombrières produisent.</li>
</ul>""",
        faq=[("Un parking en pente peut-il recevoir des ombrières ?", "Oui, dans la plupart des cas. La structure s'adapte au dénivelé, mais cela influe sur les fondations et le budget. L'installateur l'évalue lors de la visite du site."),
             ("Les sites industriels de la vallée du Gier sont-ils concernés ?", "Oui, si leur parking extérieur dépasse 1 500 m². Pour un site classé ICPE, des règles spécifiques s'appliquent et doivent être intégrées dès l'étude."),
             ("Intervenez-vous dans la plaine du Forez ?", "Oui : Andrézieux-Bouthéon, Montbrison, Saint-Just-Saint-Rambert et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['lyon', 'roanne', 'clermont-ferrand', 'valence'],
    ),
    dict(
        slug='grenoble', groupe='ville', nom='Grenoble', a='à Grenoble', dept='Isère (38)', cp='38000',
        title="Ombrière Solaire Grenoble : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Grenoble et dans le Grésivaudan : loi APER, charges de neige, financement. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Grenoble et dans le Grésivaudan</em>",
        sub="Zones commerciales, parcs technologiques, sites industriels du Grésivaudan, campus : l'agglomération grenobloise compte de nombreux parkings concernés par la loi APER, avec des contraintes de montagne à bien intégrer.",
        points=["Grenoble-Alpes Métropole et Grésivaudan", "Structures dimensionnées pour la neige", "Installateur intervenant en Isère"],
        contexte="""<h2>Les parkings concernés autour de Grenoble</h2>
<p>Coincée entre les massifs, l'agglomération grenobloise dispose de peu de foncier : les grands parkings en surface y sont d'autant plus précieux. Les couvrir d'ombrières permet de se mettre en conformité tout en produisant de l'électricité sans consommer de terrain supplémentaire.</p>""",
        sites=["Les <strong>zones commerciales</strong> du sud de l'agglomération, autour de Grand'Place et de Comboire, et du nord-ouest vers Saint-Égrève.",
               "Les <strong>sites industriels et de haute technologie</strong> du Grésivaudan, de Meylan à Crolles et Bernin, aux parkings salariés étendus.",
               "Le <strong>campus universitaire</strong> de Saint-Martin-d'Hères et la presqu'île scientifique.",
               "Les <strong>établissements de santé</strong> et les équipements sportifs de l'agglomération."],
        local="""<h2>Les spécificités d'un projet en Isère</h2>
<ul>
<li><strong>Neige :</strong> les charges de neige sont plus élevées qu'en plaine et augmentent avec l'altitude. La structure est dimensionnée en conséquence, ce qui pèse sur le budget.</li>
<li><strong>Ensoleillement :</strong> les fonds de vallée bénéficient d'un bon ensoleillement, mais les reliefs peuvent créer des ombres portées en hiver. L'étude de production en tient compte.</li>
<li><strong>Sites sensibles :</strong> les sites industriels de haute technologie imposent souvent des contraintes de sécurité et de continuité d'activité pendant le chantier.</li>
<li><strong>Autoconsommation :</strong> laboratoires, salles blanches et bureaux consomment beaucoup en journée.</li>
</ul>""",
        faq=[("La neige est-elle un problème pour une ombrière à Grenoble ?", "Non, à condition que la structure soit dimensionnée pour les charges de neige de votre site, qui dépendent de la zone climatique et de l'altitude. Cela renforce la structure et peut augmenter le budget, d'où l'intérêt d'une étude précise."),
             ("Les sites du Grésivaudan sont-ils concernés ?", "Oui, dès lors que leur parking extérieur dépasse 1 500 m². Les grands sites industriels relèvent souvent de l'échéance la plus proche."),
             ("Intervenez-vous dans tout le bassin grenoblois ?", "Oui : Grenoble, Échirolles, Saint-Martin-d'Hères, Meylan, Crolles, Voiron, Saint-Égrève et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['chambery', 'annecy', 'valence', 'saint-quentin-fallavier'],
    ),
    dict(
        slug='clermont-ferrand', groupe='ville', nom='Clermont-Ferrand', a='à Clermont-Ferrand', dept='Puy-de-Dôme (63)', cp='63000',
        title="Ombrière Solaire Clermont-Ferrand : Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Clermont-Ferrand et dans le Puy-de-Dôme : sites industriels, commerces, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Clermont-Ferrand</em>",
        sub="Grands sites industriels, zones commerciales, hôpitaux et campus : la métropole clermontoise et la plaine de la Limagne comptent de nombreux parkings concernés par la loi APER.",
        points=["Clermont Auvergne Métropole et Limagne", "Grands parkings industriels et commerciaux", "Installateur intervenant dans le Puy-de-Dôme"],
        contexte="""<h2>Les parkings concernés autour de Clermont-Ferrand</h2>
<p>Ville industrielle historique, Clermont-Ferrand compte de grands sites de production et de recherche, dont les parkings salariés dépassent souvent largement le seuil de 1 500 m². S'y ajoutent les zones commerciales de périphérie et les établissements de santé.</p>""",
        sites=["Les <strong>grands sites industriels et centres de recherche</strong> de l'agglomération, aux parkings salariés très étendus.",
               "Les <strong>zones d'activités</strong> du Brézet et de l'est clermontois, près de l'aéroport.",
               "Les <strong>zones commerciales</strong> d'Aubière, du nord de l'agglomération et de Riom.",
               "Le <strong>CHU</strong>, les cliniques et les <strong>campus universitaires</strong>."],
        local="""<h2>Les points à anticiper dans le Puy-de-Dôme</h2>
<ul>
<li><strong>Paysage :</strong> la Chaîne des Puys est inscrite au patrimoine mondial de l'UNESCO. Sur l'ouest de l'agglomération, l'insertion paysagère des ombrières mérite une attention particulière.</li>
<li><strong>Climat :</strong> les épisodes neigeux et les orages de grêle sont intégrés au dimensionnement des structures et au choix des modules.</li>
<li><strong>Grands sites :</strong> pour les parkings de plusieurs hectares, le phasage du chantier et le raccordement au réseau sont les points clés du calendrier.</li>
<li><strong>Autoconsommation :</strong> les sites industriels consomment en continu, un profil favorable pour consommer l'électricité produite.</li>
</ul>""",
        faq=[("Un très grand parking industriel doit-il être entièrement couvert ?", "Non. Pour les parkings non concédés, l'obligation porte sur au moins la moitié de la surface, avec désormais la possibilité de combiner ombrières photovoltaïques et ombrage végétal. L'implantation optimale se définit dans l'étude."),
             ("La grêle est-elle un risque pour les panneaux ?", "Les modules sont testés contre la grêle selon des normes, et certains offrent une résistance renforcée. Le choix des modules et l'assurance de l'installation tiennent compte de ce risque."),
             ("Intervenez-vous hors de la métropole ?", "Oui, dans tout le Puy-de-Dôme : Riom, Issoire, Thiers et la Limagne. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['saint-etienne', 'lyon', 'dijon', 'valence'],
    ),
    dict(
        slug='dijon', groupe='ville', nom='Dijon', a='à Dijon', dept='Côte-d\'Or (21)', cp='21000',
        title="Ombrière Solaire Dijon : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Dijon et en Côte-d'Or : zones commerciales, parcs d'activités, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Dijon et en Côte-d'Or</em>",
        sub="Zones commerciales de périphérie, parcs d'activités et logistiques, hôpitaux : la métropole dijonnaise compte de nombreux parcs de stationnement extérieurs concernés par la loi APER.",
        points=["Dijon Métropole et Côte-d'Or", "Zones commerciales et logistiques", "Installateur intervenant en Bourgogne"],
        contexte="""<h2>Les parkings concernés autour de Dijon</h2>
<p>À la croisée des axes routiers entre Paris, Lyon et l'est de la France, l'agglomération dijonnaise concentre de grandes zones commerciales et logistiques. Leurs parkings extérieurs dépassent souvent le seuil de 1 500 m², et parfois celui de 10 000 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> du nord-est de l'agglomération, autour de la Toison d'Or et de Quetigny, et du sud vers Chenôve.",
               "Les <strong>parcs d'activités et plateformes logistiques</strong> de Longvic et des abords de l'autoroute.",
               "Le <strong>CHU</strong>, les cliniques et le <strong>campus universitaire</strong>.",
               "Les <strong>parkings relais</strong> et équipements sportifs de la métropole."],
        local="""<h2>Les points à anticiper en Côte-d'Or</h2>
<ul>
<li><strong>Patrimoine :</strong> le centre historique et les Climats du vignoble de Bourgogne, inscrits à l'UNESCO, imposent une insertion soignée pour les sites proches.</li>
<li><strong>Climat :</strong> hivers frais et épisodes neigeux possibles : la structure est dimensionnée pour les charges de votre zone.</li>
<li><strong>Logistique :</strong> sur les plateformes, la hauteur libre et l'implantation des poteaux doivent laisser circuler les poids lourds.</li>
<li><strong>Autoconsommation :</strong> commerces et entrepôts frigorifiques consomment en journée, au moment où les ombrières produisent.</li>
</ul>""",
        faq=[("Les zones commerciales de Dijon sont-elles concernées ?", "Très souvent, oui : la plupart des parkings de grandes surfaces dépassent 1 500 m². L'échéance dépend de la surface, d'où l'intérêt de faire vérifier la surface réglementaire."),
             ("Peut-on garder la circulation des poids lourds sous les ombrières ?", "Oui, avec une hauteur libre et un plan d'implantation adaptés. Sur une plateforme logistique, on couvre généralement en priorité les parkings véhicules légers."),
             ("Intervenez-vous dans toute la Côte-d'Or ?", "Oui : Dijon, Chenôve, Quetigny, Longvic, Beaune et le reste du département. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['chalon-sur-saone', 'besancon', 'macon', 'lyon'],
    ),
    dict(
        slug='annecy', groupe='ville', nom='Annecy', a='à Annecy', dept='Haute-Savoie (74)', cp='74000',
        title="Ombrière Solaire Annecy : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Annecy et en Haute-Savoie : neige, paysage, loi APER, financement. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Annecy et en Haute-Savoie</em>",
        sub="Zones commerciales, parcs d'activités industriels, établissements de santé et parkings touristiques : en Haute-Savoie, les grands parkings doivent concilier loi APER, neige et paysage.",
        points=["Grand Annecy et bassin annécien", "Structures dimensionnées pour la neige", "Installateur intervenant en Haute-Savoie"],
        contexte="""<h2>Les parkings concernés autour d'Annecy</h2>
<p>Le bassin annécien associe une activité industrielle dense, de grandes zones commerciales et un fort afflux touristique. Les parkings extérieurs de plus de 1 500 m² y sont nombreux, alors que le foncier est rare : les ombrières permettent de produire de l'énergie sans artificialiser de nouveaux terrains.</p>""",
        sites=["Les <strong>zones commerciales</strong> du nord-ouest de l'agglomération, autour d'Épagny Metz-Tessy, et de Seynod.",
               "Les <strong>parcs d'activités industriels</strong> du bassin, aux parkings salariés étendus.",
               "Les <strong>établissements de santé</strong> et les <strong>parkings de loisirs et de tourisme</strong>.",
               "Les sites de la <strong>vallée de l'Arve</strong> et du <strong>Genevois</strong>, sur demande."],
        local="""<h2>Les spécificités d'un projet en Haute-Savoie</h2>
<ul>
<li><strong>Neige :</strong> les charges de neige sont élevées et augmentent avec l'altitude. Structure, pente des panneaux et gestion du déneigement se décident dès l'étude.</li>
<li><strong>Paysage et lac :</strong> les abords du lac relèvent de règles de protection renforcées. L'insertion paysagère et le choix des teintes comptent beaucoup dans l'instruction du dossier.</li>
<li><strong>Saisonnalité :</strong> pour un parking touristique, la consommation varie fortement selon la saison, ce qui oriente le choix entre autoconsommation et vente de l'électricité.</li>
<li><strong>Recharge :</strong> coupler ombrières et bornes répond à la demande d'une clientèle de plus en plus électrique.</li>
</ul>""",
        faq=[("Faut-il déneiger les ombrières ?", "En général non : la structure est dimensionnée pour supporter la neige de votre zone et la pente des panneaux aide à son évacuation. Il faut en revanche prévoir où tombe la neige, pour ne pas gêner la circulation et le déneigement du parking."),
             ("Un parking proche du lac peut-il être équipé ?", "Souvent oui, mais l'instruction est plus exigeante sur l'insertion paysagère. Une impossibilité avérée liée à des règles de protection peut aussi relever d'une exemption, à justifier."),
             ("Intervenez-vous dans toute la Haute-Savoie ?", "Oui : bassin annécien, Genevois, vallée de l'Arve et Chablais. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['annemasse', 'chambery', 'grenoble', 'lyon'],
    ),
    dict(
        slug='chambery', groupe='ville', nom='Chambéry', a='à Chambéry', dept='Savoie (73)', cp='73000',
        title="Ombrière Solaire Chambéry : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Chambéry et en Savoie : zones d'activités, Savoie Technolac, neige, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Chambéry et en Savoie</em>",
        sub="Zones commerciales, parcs d'activités, établissements de santé : dans le bassin chambérien et autour du lac du Bourget, les grands parkings doivent se préparer à la loi APER avec des contraintes de montagne.",
        points=["Grand Chambéry et Grand Lac", "Structures dimensionnées pour la neige", "Installateur intervenant en Savoie"],
        contexte="""<h2>Les parkings concernés autour de Chambéry</h2>
<p>Le bassin chambérien est un territoire pionnier du solaire : Savoie Technolac, au Bourget-du-Lac, accueille l'Institut national de l'énergie solaire. Ses zones commerciales et ses parcs d'activités comptent de nombreux parkings extérieurs de plus de 1 500 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> du nord de Chambéry et de La Ravoire.",
               "Les <strong>parcs d'activités</strong> de l'agglomération, dont Savoie Technolac et les zones de Bissy.",
               "Le <strong>centre hospitalier</strong>, les cliniques et le campus universitaire.",
               "Les sites d'<strong>Aix-les-Bains</strong> et de la combe de Savoie, sur demande."],
        local="""<h2>Les spécificités d'un projet en Savoie</h2>
<ul>
<li><strong>Neige :</strong> les charges de neige, plus fortes qu'en plaine, conditionnent la structure et le budget. Elles dépendent de l'altitude précise du site.</li>
<li><strong>Paysage :</strong> autour du lac du Bourget, des règles de protection du littoral lacustre s'appliquent : l'insertion du projet doit être soignée.</li>
<li><strong>Relief :</strong> l'orientation de la vallée et les ombres portées des massifs sont intégrées à l'estimation de la production.</li>
<li><strong>Écosystème local :</strong> la présence d'acteurs spécialisés du solaire facilite l'accès à des compétences techniques pointues.</li>
</ul>""",
        faq=[("Les ombrières résistent-elles aux hivers savoyards ?", "Oui, à condition d'être dimensionnées pour les charges de neige et de vent de votre site. C'est une étape centrale de l'étude technique, qui influe sur le budget."),
             ("Un parking à Aix-les-Bains ou près du lac est-il concerné ?", "Oui, s'il dépasse 1 500 m² en extérieur. Près du lac, l'insertion paysagère fait l'objet d'une attention particulière lors de l'instruction du dossier."),
             ("Intervenez-vous dans toute la Savoie ?", "Oui : Chambéry, Aix-les-Bains, la combe de Savoie et les vallées. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['annecy', 'grenoble', 'lyon', 'saint-quentin-fallavier'],
    ),
    dict(
        slug='valence', groupe='ville', nom='Valence', a='à Valence', dept='Drôme (26)', cp='26000',
        title="Ombrière Solaire Valence : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Valence et dans la Drôme : fort ensoleillement, vent, loi APER, financement. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Valence et dans la Drôme</em>",
        sub="Zones commerciales, parcs d'activités, plateformes logistiques le long de l'A7 : la vallée du Rhône drômoise combine grands parkings et fort ensoleillement, idéal pour des ombrières productives.",
        points=["Valence Romans Agglo et vallée du Rhône", "Un ensoleillement parmi les meilleurs de la région", "Installateur intervenant dans la Drôme et l'Ardèche"],
        contexte="""<h2>Les parkings concernés autour de Valence</h2>
<p>Porte du Midi, Valence bénéficie d'un ensoleillement nettement supérieur à celui du nord de la région. Pour un propriétaire de parking, l'obligation de la loi APER s'accompagne donc d'une production d'électricité plus élevée, qui améliore la rentabilité du projet.</p>""",
        sites=["Les <strong>zones commerciales</strong> de périphérie, à Valence, Romans-sur-Isère et Guilherand-Granges.",
               "Le <strong>parc d'activités de Rovaltain</strong>, près de la gare TGV, et les zones d'activités de l'agglomération.",
               "Les <strong>plateformes logistiques</strong> implantées le long de l'A7 et de la vallée du Rhône.",
               "Le <strong>centre hospitalier</strong>, les campus et les équipements sportifs."],
        local="""<h2>Les spécificités d'un projet dans la Drôme</h2>
<ul>
<li><strong>Vent :</strong> le couloir rhodanien est exposé à des vents du nord soutenus. La structure et les fondations sont dimensionnées pour ces efforts.</li>
<li><strong>Chaleur :</strong> les étés chauds rendent l'ombrage très apprécié des clients et des salariés, et limitent l'échauffement des véhicules.</li>
<li><strong>Production :</strong> le fort ensoleillement améliore le rendement, ce qui rend la vente totale comme l'autoconsommation intéressantes.</li>
<li><strong>Agro-industrie :</strong> les sites de transformation et de froid consomment en journée, un profil idéal pour l'autoconsommation.</li>
</ul>""",
        faq=[("Le vent de la vallée du Rhône est-il un problème ?", "Non, il est pris en compte dans le dimensionnement de la structure et des fondations, selon la zone de vent réglementaire de votre site. Cela peut renforcer la structure et donc influer sur le budget."),
             ("Une ombrière est-elle plus rentable à Valence qu'à Lyon ?", "À installation égale, la production est généralement plus élevée grâce au meilleur ensoleillement. La rentabilité dépend aussi du coût de la structure, du raccordement et du mode de valorisation : seule l'étude permet de comparer."),
             ("Intervenez-vous en Ardèche et dans le sud de la Drôme ?", "Oui : Valence, Romans-sur-Isère, Guilherand-Granges, Montélimar et le nord de l'Ardèche. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['montelimar', 'avignon', 'grenoble', 'vienne'],
    ),
    # ------------------------------------------------------- PÔLES D'ACTIVITÉS
    dict(
        slug='saint-priest', groupe='pole', nom='Saint-Priest et Bron', a='à Saint-Priest, Bron et Chassieu', dept='Rhône (69)', cp='69800',
        title="Ombrière Solaire Saint-Priest, Bron, Chassieu",
        desc="Ombrières photovoltaïques pour parkings à Saint-Priest, Bron et Chassieu : zones commerciales, parcs technologiques, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Saint-Priest, Bron et Chassieu</em>",
        sub="Zones commerciales, parcs technologiques, sites d'exposition et d'activités : l'est lyonnais concentre certains des plus grands parkings extérieurs de la région, souvent concernés par l'échéance la plus proche.",
        points=["Est lyonnais : Saint-Priest, Bron, Chassieu, Genas", "Parkings de plus de 10 000 m² fréquents", "Installateur intervenant dans le Rhône"],
        contexte="""<h2>Un secteur aux très grands parkings</h2>
<p>L'est lyonnais est l'un des premiers pôles d'activités de l'agglomération. On y trouve des parkings de plusieurs hectares, pour les clients des zones commerciales, les salariés des parcs d'activités ou les visiteurs des grands équipements. Beaucoup dépassent 10 000 m² et relèvent de l'échéance la plus proche.</p>""",
        sites=["Les <strong>zones commerciales de la Porte des Alpes</strong>, entre Saint-Priest, Bron et Chassieu.",
               "Le <strong>parc technologique de Saint-Priest</strong> et les parcs tertiaires voisins.",
               "Les <strong>zones industrielles et logistiques</strong> de Mi-Plaine et de Genas.",
               "Les <strong>grands équipements</strong> d'exposition et de loisirs, dont les parkings visiteurs sont parmi les plus vastes de la région."],
        local="""<h2>Ce qui compte pour un projet dans l'est lyonnais</h2>
<ul>
<li><strong>Échéance :</strong> les parkings de plus de 10 000 m² étaient concernés dès le 1er juillet 2026. Des délais existent sous conditions : lancer l'étude rapidement est la meilleure façon d'en bénéficier.</li>
<li><strong>Raccordement :</strong> pour des puissances importantes, la demande de raccordement et les éventuels travaux de réseau pèsent sur le calendrier.</li>
<li><strong>Exploitation :</strong> pour un parking utilisé en continu ou lors d'événements, le chantier doit être phasé pour maintenir l'accès.</li>
<li><strong>Recharge :</strong> sur un parking salariés ou clients, des bornes sous ombrières valorisent directement l'électricité produite.</li>
</ul>""",
        faq=[("Mon parking de zone commerciale dépasse 10 000 m², suis-je en retard ?", "L'échéance des plus grands parkings était fixée au 1er juillet 2026, mais des délais supplémentaires sont prévus sous conditions, notamment pour les projets engagés. Faites vérifier votre situation rapidement."),
             ("Un parking utilisé pour des événements peut-il être équipé ?", "Oui. Le phasage des travaux et l'implantation des poteaux sont adaptés aux flux de véhicules et aux périodes d'affluence."),
             ("Quelles communes couvrez-vous dans l'est lyonnais ?", "Saint-Priest, Bron, Chassieu, Genas, Mions, Corbas et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['lyon', 'saint-quentin-fallavier', 'limonest', 'plaine-de-l-ain'],
    ),
    dict(
        slug='saint-quentin-fallavier', groupe='pole', nom='Saint-Quentin-Fallavier et L\'Isle-d\'Abeau', a='à Saint-Quentin-Fallavier et L\'Isle-d\'Abeau', dept='Isère (38)', cp='38070',
        title="Ombrière Solaire Saint-Quentin-Fallavier, Isle-d'Abeau",
        desc="Ombrières photovoltaïques pour parkings logistiques à Saint-Quentin-Fallavier, L'Isle-d'Abeau et dans le Nord-Isère. Loi APER, étude gratuite.",
        h1="Ombrières solaires pour la logistique <em>à Saint-Quentin-Fallavier et L'Isle-d'Abeau</em>",
        sub="Le Nord-Isère accueille l'un des plus grands pôles logistiques de France. Parkings salariés, parcs poids lourds, zones d'attente : des surfaces importantes, souvent concernées par la loi APER.",
        points=["Parc de Chesnes et agglomération Porte de l'Isère", "Plateformes logistiques et industrielles", "Installateur intervenant dans le Nord-Isère"],
        contexte="""<h2>Un pôle logistique majeur</h2>
<p>Entre l'aéroport Lyon-Saint-Exupéry et l'agglomération Porte de l'Isère, le <strong>parc international de Chesnes</strong> et les zones voisines regroupent un très grand nombre d'entrepôts et de plateformes. Leurs parkings salariés et leurs aires de stationnement dépassent fréquemment le seuil de la loi APER.</p>""",
        sites=["Les <strong>plateformes logistiques</strong> du parc de Chesnes, à Saint-Quentin-Fallavier et dans les communes voisines.",
               "Les <strong>sites industriels</strong> et parcs d'activités de L'Isle-d'Abeau, Villefontaine et Bourgoin-Jallieu.",
               "Les <strong>zones commerciales</strong> de l'agglomération Porte de l'Isère.",
               "Le <strong>centre hospitalier</strong> et les équipements publics du Nord-Isère."],
        local="""<h2>Les spécificités d'un parking logistique</h2>
<ul>
<li><strong>Quelles surfaces couvrir :</strong> on privilégie en général les parkings véhicules légers des salariés. Les cours de manœuvre des poids lourds se prêtent moins aux ombrières.</li>
<li><strong>Hauteur et poteaux :</strong> l'implantation doit préserver la circulation, la visibilité et la sécurité des engins.</li>
<li><strong>ICPE :</strong> de nombreux entrepôts sont classés et soumis à des règles de distance autour des stockages, qui peuvent modifier la surface concernée.</li>
<li><strong>Bail et propriétaire :</strong> entre la foncière propriétaire et le logisticien locataire, le bail précise souvent qui porte l'obligation et qui profite de l'électricité.</li>
</ul>""",
        faq=[("Les zones de manœuvre des camions comptent-elles dans la surface ?", "Les règles de calcul de la surface sont précises et prévoient des exclusions. Pour un site logistique, il faut distinguer les parkings, les voies et les zones de manœuvre : faites vérifier la surface réglementaire sur plan."),
             ("Qui doit agir, le propriétaire ou le logisticien ?", "En principe le propriétaire du parc de stationnement, mais le bail peut répartir les obligations différemment. Échangez tôt avec la foncière ou le locataire selon votre position."),
             ("Quelles communes couvrez-vous dans le Nord-Isère ?", "Saint-Quentin-Fallavier, L'Isle-d'Abeau, Villefontaine, Bourgoin-Jallieu, Satolas-et-Bonce et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['saint-priest', 'plaine-de-l-ain', 'lyon', 'grenoble'],
    ),
    dict(
        slug='plaine-de-l-ain', groupe='pole', nom='Plaine de l\'Ain', a='dans la Plaine de l\'Ain', dept='Ain (01)', cp='01150',
        title="Ombrière Solaire Plaine de l'Ain : Parkings Industriels",
        desc="Ombrières photovoltaïques pour parkings industriels et logistiques dans la Plaine de l'Ain et l'Ain : loi APER, ICPE, financement. Étude gratuite.",
        h1="Ombrières solaires de parking <em>dans la Plaine de l'Ain</em>",
        sub="Parc industriel de la Plaine de l'Ain, zones logistiques, sites de production : les parkings salariés et aires de stationnement de l'Ain sont nombreux à dépasser le seuil de la loi APER.",
        points=["Parc industriel de la Plaine de l'Ain et environs", "Sites industriels, chimiques et logistiques", "Installateur intervenant dans l'Ain"],
        contexte="""<h2>Un grand parc industriel aux portes de Lyon</h2>
<p>Le <strong>parc industriel de la Plaine de l'Ain</strong>, autour de Saint-Vulbas et Blyes, réunit des entreprises industrielles et logistiques de premier plan. Leurs sites disposent de vastes parkings salariés, souvent concernés par l'obligation d'ombrières.</p>""",
        sites=["Les <strong>sites industriels et logistiques</strong> du parc de la Plaine de l'Ain.",
               "Les <strong>zones d'activités</strong> d'Ambérieu-en-Bugey, de Lagnieu et de la Côtière.",
               "Les <strong>zones commerciales</strong> de Bourg-en-Bresse et de Miribel, sur demande.",
               "Les <strong>équipements publics</strong> et établissements de santé du département."],
        local="""<h2>Les points à anticiper dans un parc industriel</h2>
<ul>
<li><strong>Sites classés :</strong> beaucoup d'installations relèvent de la réglementation ICPE, avec des règles de distance et de sécurité qui conditionnent l'implantation.</li>
<li><strong>Consignes de sûreté :</strong> sur certains sites, l'accès des entreprises extérieures et le déroulement du chantier sont strictement encadrés.</li>
<li><strong>Autoconsommation :</strong> les process industriels consomment en continu : l'électricité produite peut être consommée sur place.</li>
<li><strong>Autoconsommation collective :</strong> dans un parc d'activités, partager la production entre plusieurs entreprises voisines est une option à étudier.</li>
</ul>""",
        faq=[("Un site industriel classé peut-il installer des ombrières ?", "Oui, dans la plupart des cas, mais des règles de distance autour de certaines installations s'appliquent. Elles peuvent aussi réduire la surface concernée par l'obligation : l'étude doit les intégrer dès le départ."),
             ("Peut-on partager l'électricité avec les entreprises voisines ?", "Oui, via l'autoconsommation collective, sous conditions de proximité. C'est une piste intéressante dans un parc d'activités, à étudier avec l'installateur."),
             ("Quelles communes couvrez-vous dans l'Ain ?", "Saint-Vulbas, Blyes, Ambérieu-en-Bugey, Lagnieu, Montluel, Miribel, Bourg-en-Bresse et le reste du département. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['bourg-en-bresse', 'saint-quentin-fallavier', 'saint-priest', 'lyon'],
    ),
    dict(
        slug='limonest', groupe='pole', nom='Limonest et Dardilly', a='à Limonest et Dardilly', dept='Rhône (69)', cp='69760',
        title="Ombrière Solaire Limonest, Dardilly : Parkings",
        desc="Ombrières photovoltaïques pour parkings à Limonest, Dardilly et dans l'ouest lyonnais : parcs tertiaires, zones commerciales, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Limonest et Dardilly</em>",
        sub="Parcs tertiaires, sièges d'entreprises et zones commerciales du nord-ouest lyonnais : des parkings salariés et clients souvent concernés par la loi APER, dans un cadre paysager à respecter.",
        points=["Techlid, Porte de Lyon et ouest lyonnais", "Parcs tertiaires et sièges sociaux", "Installateur intervenant dans le Rhône"],
        contexte="""<h2>Le pôle tertiaire du nord-ouest lyonnais</h2>
<p>Autour de Limonest, Dardilly et Champagne-au-Mont-d'Or, le <strong>parc Techlid</strong> et la <strong>zone de la Porte de Lyon</strong> accueillent de nombreux sièges d'entreprises, bureaux et commerces. Leurs parkings en surface dépassent souvent 1 500 m².</p>""",
        sites=["Les <strong>parcs tertiaires</strong> de Techlid, à Limonest, Dardilly et Champagne-au-Mont-d'Or.",
               "Les <strong>zones commerciales</strong> de la Porte de Lyon et des abords de l'autoroute.",
               "Les <strong>sièges sociaux</strong> et campus d'entreprises de l'ouest lyonnais, jusqu'à Écully.",
               "Les <strong>établissements d'enseignement</strong> et de santé du secteur."],
        local="""<h2>Les spécificités d'un projet dans l'ouest lyonnais</h2>
<ul>
<li><strong>Cadre paysager :</strong> les parcs tertiaires sont souvent arborés. L'ombrage végétal existant et la combinaison arbres-ombrières sont à intégrer au projet.</li>
<li><strong>Relief :</strong> les parkings en terrasses des Monts d'Or demandent une structure adaptée au terrain.</li>
<li><strong>Bureaux :</strong> les bâtiments tertiaires consomment surtout en journée, en semaine : un profil très favorable à l'autoconsommation.</li>
<li><strong>Mobilité :</strong> les salariés viennent souvent en voiture : des bornes sous ombrières accompagnent l'électrification des flottes et des véhicules personnels.</li>
</ul>""",
        faq=[("Mon parking est déjà arboré, suis-je concerné ?", "Un parking déjà ombragé à plus de 50 % par des arbres peut relever d'une exemption, à justifier. Sinon, l'ombrage végétal peut désormais compléter les ombrières photovoltaïques dans certaines limites."),
             ("Plusieurs entreprises partagent le parking : comment faire ?", "Il faut d'abord identifier le propriétaire du parc de stationnement, souvent la copropriété ou la foncière. Le projet et le partage de l'électricité se décident ensuite entre les occupants."),
             ("Quelles communes couvrez-vous dans l'ouest lyonnais ?", "Limonest, Dardilly, Champagne-au-Mont-d'Or, Écully, Tassin-la-Demi-Lune et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['lyon', 'saint-priest', 'plaine-de-l-ain', 'saint-etienne'],
    ),
    # ------------------------------------------------------------- VAGUE 2
    dict(
        slug='villefranche-sur-saone', groupe='ville2', nom='Villefranche-sur-Saône', a='à Villefranche-sur-Saône', dept='Rhône (69)', cp='69400',
        title="Ombrière Solaire Villefranche-sur-Saône : Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Villefranche-sur-Saône et dans le Beaujolais : zones d'activités, commerces, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Villefranche-sur-Saône</em>",
        sub="Zones commerciales, parcs d'activités le long de l'A6, sites industriels et agroalimentaires : entre Saône et Beaujolais, de nombreux parkings dépassent le seuil de la loi APER.",
        points=["Agglomération de Villefranche et Val de Saône", "Zones d'activités de l'axe A6", "Installateur intervenant dans le nord du Rhône"],
        contexte="""<h2>Les parkings concernés autour de Villefranche</h2>
<p>Capitale du Beaujolais, Villefranche-sur-Saône s'est développée le long de l'A6 et de la Saône. Ses zones d'activités et ses zones commerciales, réparties entre Villefranche, Arnas, Gleizé et Limas, comptent de nombreux parkings extérieurs de plus de 1 500 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> de l'agglomération caladoise, aux parkings clients étendus.",
               "Les <strong>parcs d'activités</strong> d'Arnas et des abords de l'A6, avec des sites logistiques et industriels.",
               "Les <strong>sites agroalimentaires et viticoles</strong> du Beaujolais et du Val de Saône.",
               "L'<strong>hôpital</strong> et les équipements publics de l'agglomération."],
        local="""<h2>Les points à anticiper dans le Beaujolais</h2>
<ul>
<li><strong>Zones inondables :</strong> une partie de la plaine de Saône est couverte par un plan de prévention des risques d'inondation, qui encadre l'implantation et la conception des structures.</li>
<li><strong>Paysage :</strong> sur les coteaux du Beaujolais, l'insertion des ombrières dans le paysage viticole mérite une attention particulière.</li>
<li><strong>Logistique :</strong> sur les sites de l'axe A6, l'implantation doit préserver la circulation des poids lourds.</li>
<li><strong>Autoconsommation :</strong> commerces et sites de production consomment en journée, au moment où les ombrières produisent.</li>
</ul>""",
        faq=[("Un parking en zone inondable peut-il recevoir des ombrières ?", "Souvent oui, mais le plan de prévention des risques impose des règles : hauteur des équipements électriques, transparence hydraulique des structures, parfois des restrictions d'implantation. L'étude doit vérifier ces règles dès le départ."),
             ("Les caves et sites viticoles sont-ils concernés ?", "Oui, si leur parking extérieur dépasse 1 500 m², ce qui arrive pour les grands sites d'accueil ou de production. Les plus petits parkings ne sont pas concernés par l'obligation."),
             ("Quelles communes couvrez-vous autour de Villefranche ?", "Villefranche-sur-Saône, Arnas, Gleizé, Limas, Anse, Belleville-en-Beaujolais et le Val de Saône. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['macon', 'lyon', 'limonest', 'bourg-en-bresse'],
    ),
    dict(
        slug='vienne', groupe='ville2', nom='Vienne', a='à Vienne', dept='Isère (38)', cp='38200',
        title="Ombrière Solaire Vienne : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Vienne et dans la vallée du Rhône : sites industriels, commerces, patrimoine, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Vienne et dans la vallée du Rhône</em>",
        sub="Zones commerciales, sites industriels et chimiques du couloir rhodanien, établissements de santé : autour de Vienne, les grands parkings doivent concilier loi APER, patrimoine et risques naturels.",
        points=["Vienne Condrieu Agglomération et pays roussillonnais", "Sites industriels et chimiques", "Installateur intervenant dans le nord de l'Isère"],
        contexte="""<h2>Les parkings concernés autour de Vienne</h2>
<p>Au sud de Lyon, le long du Rhône et de l'A7, l'agglomération viennoise et le pays roussillonnais combinent zones commerciales, parcs d'activités et grands sites industriels. Leurs parkings salariés et clients dépassent souvent le seuil de 1 500 m².</p>""",
        sites=["Les <strong>zones commerciales et d'activités</strong> de Vienne, Chasse-sur-Rhône et Estrablin.",
               "Les <strong>sites industriels et chimiques</strong> du couloir rhodanien, dont la plateforme de Roussillon.",
               "Les <strong>sites logistiques</strong> implantés le long de l'A7.",
               "Le <strong>centre hospitalier</strong> et les équipements publics de l'agglomération."],
        local="""<h2>Les points à anticiper autour de Vienne</h2>
<ul>
<li><strong>Patrimoine :</strong> Vienne possède un riche patrimoine antique et médiéval. À proximité des monuments protégés, l'avis de l'architecte des Bâtiments de France peut être requis.</li>
<li><strong>Rhône :</strong> les zones proches du fleuve peuvent être soumises à un plan de prévention des risques d'inondation, et le couloir est exposé à des vents du nord soutenus.</li>
<li><strong>Sites industriels :</strong> les sites classés ICPE ou Seveso imposent des règles de distance et de sécurité, qui conditionnent l'implantation et le déroulement du chantier.</li>
<li><strong>Autoconsommation :</strong> les process industriels consomment en continu : une grande partie de la production peut être consommée sur place.</li>
</ul>""",
        faq=[("Un site Seveso peut-il installer des ombrières ?", "C'est possible, mais l'implantation doit respecter les règles de sécurité du site et les distances autour des installations à risque. Ces contraintes peuvent aussi modifier la surface concernée : elles s'étudient avec le service sécurité du site."),
             ("Faut-il l'accord de l'architecte des Bâtiments de France ?", "Seulement si le parking se trouve dans le périmètre d'un monument protégé ou d'un site patrimonial remarquable. L'installateur vérifie ce point avant de déposer l'autorisation d'urbanisme."),
             ("Quelles communes couvrez-vous autour de Vienne ?", "Vienne, Chasse-sur-Rhône, Estrablin, Pont-Évêque, Roussillon, Salaise-sur-Sanne, Condrieu et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['lyon', 'saint-priest', 'saint-etienne', 'valence'],
    ),
    dict(
        slug='bourg-en-bresse', groupe='ville2', nom='Bourg-en-Bresse', a='à Bourg-en-Bresse', dept='Ain (01)', cp='01000',
        title="Ombrière Solaire Bourg-en-Bresse : Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Bourg-en-Bresse et dans l'Ain : zones commerciales, industrie, agroalimentaire, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Bourg-en-Bresse</em>",
        sub="Zones commerciales de périphérie, sites industriels et agroalimentaires, établissements de santé : dans l'agglomération burgienne, de nombreux parkings sont concernés par la loi APER.",
        points=["Grand Bourg Agglomération et Bresse", "Industrie et agroalimentaire", "Installateur intervenant dans l'Ain"],
        contexte="""<h2>Les parkings concernés autour de Bourg-en-Bresse</h2>
<p>Préfecture de l'Ain, Bourg-en-Bresse concentre les zones commerciales du département et un tissu industriel et agroalimentaire important. Les parkings de ces sites dépassent régulièrement le seuil de 1 500 m², et parfois celui de 10 000 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> de périphérie, à Viriat, Saint-Denis-lès-Bourg et Péronnas.",
               "Les <strong>sites industriels</strong> de l'agglomération, aux parkings salariés étendus.",
               "Les <strong>sites agroalimentaires</strong> de la Bresse.",
               "Le <strong>centre hospitalier</strong>, les établissements scolaires et les équipements sportifs."],
        local="""<h2>Les points à anticiper dans la Bresse</h2>
<ul>
<li><strong>Terrain :</strong> les sols argileux et humides de la Bresse influencent le choix des fondations, à vérifier par une étude de sol.</li>
<li><strong>Climat :</strong> hivers frais, brouillards et épisodes neigeux sont intégrés au dimensionnement et à l'estimation de la production.</li>
<li><strong>Agroalimentaire :</strong> les besoins de froid et de process en journée offrent un bon profil d'autoconsommation.</li>
<li><strong>Commerces :</strong> sur les parkings clients, le chantier est phasé par zones pour maintenir l'accès.</li>
</ul>""",
        faq=[("Le sol de mon parking influence-t-il le projet ?", "Oui. La nature du sol conditionne le type et la taille des fondations, donc une partie du budget. Une étude de sol est généralement réalisée avant de finaliser la conception."),
             ("Un site agroalimentaire a-t-il intérêt à autoconsommer ?", "Souvent oui : le froid et les process consomment beaucoup en journée, au moment où les ombrières produisent. L'étude compare autoconsommation et vente totale à partir de vos consommations réelles."),
             ("Quelles communes couvrez-vous autour de Bourg-en-Bresse ?", "Bourg-en-Bresse, Viriat, Péronnas, Saint-Denis-lès-Bourg, Ceyzériat et toute la Bresse. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['plaine-de-l-ain', 'macon', 'lyon', 'villefranche-sur-saone'],
    ),
    dict(
        slug='macon', groupe='ville2', nom='Mâcon', a='à Mâcon', dept='Saône-et-Loire (71)', cp='71000',
        title="Ombrière Solaire Mâcon : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Mâcon et dans le Mâconnais : zones commerciales, logistique A6-A40, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Mâcon et dans le Mâconnais</em>",
        sub="Au croisement de l'A6 et de l'A40, l'agglomération mâconnaise accueille zones commerciales, plateformes logistiques et parcs d'activités, dont les parkings sont souvent concernés par la loi APER.",
        points=["Mâconnais Beaujolais Agglomération", "Plateformes logistiques A6-A40", "Installateur intervenant en Saône-et-Loire"],
        contexte="""<h2>Les parkings concernés autour de Mâcon</h2>
<p>Carrefour autoroutier entre Paris, Lyon, Genève et les Alpes, Mâcon a attiré de nombreuses activités logistiques et commerciales. Leurs parkings salariés et clients dépassent fréquemment le seuil de 1 500 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> du nord et du sud de l'agglomération, à Crêches-sur-Saône, Sancé et Charnay-lès-Mâcon.",
               "Les <strong>plateformes logistiques et parcs d'activités</strong> proches des échangeurs de l'A6 et de l'A40.",
               "Les <strong>caves coopératives et sites viticoles</strong> du Mâconnais.",
               "Le <strong>centre hospitalier</strong> et les équipements publics."],
        local="""<h2>Les points à anticiper dans le Mâconnais</h2>
<ul>
<li><strong>Zones inondables :</strong> les abords de la Saône peuvent être soumis à un plan de prévention des risques d'inondation, qui encadre la conception des structures.</li>
<li><strong>Logistique :</strong> la hauteur libre et l'implantation des poteaux sont adaptées à la circulation des poids lourds.</li>
<li><strong>Paysage viticole :</strong> sur les coteaux, l'insertion paysagère est à soigner.</li>
<li><strong>Recharge :</strong> sur un axe de transit majeur, des bornes sous ombrières peuvent servir les clients comme les flottes.</li>
</ul>""",
        faq=[("Les plateformes logistiques de l'A6 sont-elles concernées ?", "Oui, dès lors que leur parking extérieur dépasse 1 500 m². On couvre généralement en priorité les parkings véhicules légers des salariés, les zones de manœuvre se prêtant moins aux ombrières."),
             ("Un parking proche de la Saône peut-il être équipé ?", "Souvent oui, en respectant les règles du plan de prévention des risques d'inondation : position des équipements électriques, conception des structures. L'étude le vérifie dès le départ."),
             ("Quelles communes couvrez-vous autour de Mâcon ?", "Mâcon, Charnay-lès-Mâcon, Sancé, Crêches-sur-Saône, Replonges, Tournus et le Mâconnais. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['villefranche-sur-saone', 'bourg-en-bresse', 'chalon-sur-saone', 'lyon'],
    ),
    dict(
        slug='roanne', groupe='ville2', nom='Roanne', a='à Roanne', dept='Loire (42)', cp='42300',
        title="Ombrière Solaire Roanne : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Roanne et dans le Roannais : industrie, zones commerciales, loi APER, financement. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Roanne et dans le Roannais</em>",
        sub="Sites industriels, zones commerciales, établissements de santé : dans l'agglomération roannaise, les parkings de plus de 1 500 m² doivent se préparer à l'obligation d'ombrières.",
        points=["Roannais Agglomération", "Sites industriels et commerciaux", "Installateur intervenant dans la Loire"],
        contexte="""<h2>Les parkings concernés autour de Roanne</h2>
<p>Bassin industriel historique, le Roannais compte des sites de mécanique, de textile, de défense et d'agroalimentaire, ainsi que des zones commerciales qui attirent toute la clientèle du nord de la Loire. Beaucoup de leurs parkings dépassent le seuil de la loi APER.</p>""",
        sites=["Les <strong>zones commerciales</strong> de Mably, Riorges et du Coteau.",
               "Les <strong>sites industriels</strong> de l'agglomération, aux parkings salariés étendus.",
               "Les <strong>parcs d'activités</strong> du Roannais.",
               "Le <strong>centre hospitalier</strong> et les équipements publics."],
        local="""<h2>Les points à anticiper dans le Roannais</h2>
<ul>
<li><strong>Sites sensibles :</strong> certains sites industriels imposent des règles strictes d'accès et de sécurité, qui organisent le chantier.</li>
<li><strong>Climat :</strong> les épisodes neigeux et les orages sont intégrés au dimensionnement des structures.</li>
<li><strong>Loire :</strong> les terrains proches du fleuve peuvent être soumis à un plan de prévention des risques d'inondation.</li>
<li><strong>Autoconsommation :</strong> ateliers et sites de production consomment en journée, au moment où les ombrières produisent.</li>
</ul>""",
        faq=[("Un site industriel à accès réglementé peut-il être équipé ?", "Oui. Le chantier est alors organisé selon les règles du site : habilitations, horaires, zones d'accès. Ces contraintes se prévoient dès l'étude et dans le planning."),
             ("Mon parking fait environ 1 500 m², suis-je concerné ?", "Près du seuil, quelques mètres carrés font la différence. La surface réglementaire se calcule selon des règles précises : faites-la vérifier sur plan avant de décider."),
             ("Quelles communes couvrez-vous dans le Roannais ?", "Roanne, Mably, Riorges, Le Coteau, Charlieu et les communes voisines. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['saint-etienne', 'lyon', 'villefranche-sur-saone', 'clermont-ferrand'],
    ),
    dict(
        slug='chalon-sur-saone', groupe='ville2', nom='Chalon-sur-Saône', a='à Chalon-sur-Saône', dept='Saône-et-Loire (71)', cp='71100',
        title="Ombrière Solaire Chalon-sur-Saône : Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Chalon-sur-Saône : industrie, logistique, zones commerciales, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Chalon-sur-Saône</em>",
        sub="Grands sites industriels, plateformes logistiques le long de l'A6, zones commerciales : l'agglomération chalonnaise compte de nombreux parkings concernés par la loi APER.",
        points=["Le Grand Chalon et Bresse chalonnaise", "Industrie et logistique de l'axe A6", "Installateur intervenant en Saône-et-Loire"],
        contexte="""<h2>Les parkings concernés autour de Chalon-sur-Saône</h2>
<p>Pôle industriel et logistique de la Saône-et-Loire, Chalon-sur-Saône accueille des sites de production de taille importante et des plateformes implantées le long de l'A6. Leurs parkings salariés dépassent souvent le seuil de 1 500 m², parfois celui de 10 000 m².</p>""",
        sites=["Les <strong>grands sites industriels</strong> de l'agglomération, dont ceux de Saint-Marcel.",
               "Les <strong>plateformes logistiques</strong> du sud de l'agglomération et des abords de l'A6.",
               "Les <strong>zones commerciales</strong> du nord et du sud de Chalon.",
               "Le <strong>centre hospitalier</strong> et les équipements publics."],
        local="""<h2>Les points à anticiper autour de Chalon</h2>
<ul>
<li><strong>Zones inondables :</strong> la plaine de la Saône est en partie couverte par un plan de prévention des risques d'inondation, à intégrer dès la conception.</li>
<li><strong>Grands sites :</strong> pour les parkings de plusieurs hectares, le raccordement au réseau et le phasage du chantier structurent le calendrier.</li>
<li><strong>Logistique :</strong> l'implantation des poteaux et la hauteur libre préservent la circulation des engins.</li>
<li><strong>Autoconsommation :</strong> les sites industriels consomment en continu, un profil favorable pour consommer l'électricité produite.</li>
</ul>""",
        faq=[("Mon parking dépasse 10 000 m², quelle est mon échéance ?", "Pour les parkings non concédés de plus de 10 000 m², l'échéance était fixée au 1er juillet 2026, avec des délais possibles sous conditions, notamment pour les projets engagés. Faites vérifier votre situation rapidement."),
             ("Le raccordement est-il long pour un grand parking ?", "Il peut l'être, surtout si la puissance demande des travaux sur le réseau. C'est souvent l'étape qui fixe le calendrier : la demande se prépare dès l'étude."),
             ("Quelles communes couvrez-vous autour de Chalon ?", "Chalon-sur-Saône, Saint-Marcel, Champforgeuil, Saint-Rémy, Sevrey, Chatenoy-le-Royal et le Chalonnais. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['macon', 'dijon', 'besancon', 'bourg-en-bresse'],
    ),
    dict(
        slug='annemasse', groupe='ville2', nom='Annemasse', a='à Annemasse', dept='Haute-Savoie (74)', cp='74100',
        title="Ombrière Solaire Annemasse : Genevois et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Annemasse et dans le Genevois français : commerces, parkings relais, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Annemasse et dans le Genevois français</em>",
        sub="Zones commerciales, parcs d'activités, parkings relais des frontaliers : dans l'agglomération d'Annemasse, la pression foncière fait des grands parkings un gisement solaire précieux.",
        points=["Annemasse Agglo et Genevois français", "Zones commerciales et parkings relais", "Installateur intervenant en Haute-Savoie"],
        contexte="""<h2>Les parkings concernés autour d'Annemasse</h2>
<p>Aux portes de Genève, l'agglomération d'Annemasse connaît une forte croissance et un foncier rare. Les grands parkings en surface, commerciaux ou liés aux déplacements des frontaliers, sont des sites idéaux pour produire de l'électricité sans consommer de terrain.</p>""",
        sites=["Les <strong>zones commerciales</strong> d'Étrembières, de Ville-la-Grand et de Gaillard.",
               "Les <strong>parcs d'activités</strong> de l'agglomération et du Genevois français.",
               "Les <strong>parkings relais</strong> utilisés par les frontaliers.",
               "Le <strong>centre hospitalier</strong> et les équipements publics."],
        local="""<h2>Les spécificités d'un projet dans le Genevois</h2>
<ul>
<li><strong>Neige :</strong> les charges de neige de la Haute-Savoie sont intégrées au dimensionnement de la structure.</li>
<li><strong>Usage du parking :</strong> un parking relais occupé en journée par des véhicules de frontaliers se prête bien à l'installation de bornes de recharge.</li>
<li><strong>Foncier :</strong> la rareté du terrain rend la double fonction de l'ombrière, stationnement et production, particulièrement intéressante.</li>
<li><strong>Urbanisme :</strong> les règles des PLU de l'agglomération encadrent hauteur et aspect des structures.</li>
</ul>""",
        faq=[("Un parking relais peut-il être équipé de bornes sous ombrières ?", "Oui, et c'est un usage cohérent : les véhicules restent garés toute la journée, au moment où les ombrières produisent. Le nombre de bornes et leur puissance se dimensionnent dans l'étude."),
             ("Les ombrières résistent-elles à la neige de Haute-Savoie ?", "Oui, à condition d'être dimensionnées pour les charges de neige de votre site, qui dépendent de la zone climatique et de l'altitude. Cela peut renforcer la structure et augmenter le budget."),
             ("Quelles communes couvrez-vous dans le Genevois ?", "Annemasse, Gaillard, Ville-la-Grand, Étrembières, Saint-Julien-en-Genevois, Thonon-les-Bains et le Chablais. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['annecy', 'chambery', 'besancon', 'plaine-de-l-ain'],
    ),
    dict(
        slug='montelimar', groupe='ville2', nom='Montélimar', a='à Montélimar', dept='Drôme (26)', cp='26200',
        title="Ombrière Solaire Montélimar : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Montélimar et dans le sud de la Drôme : fort ensoleillement, mistral, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Montélimar et dans le sud de la Drôme</em>",
        sub="Zones commerciales, sites industriels et logistiques de la vallée du Rhône, établissements de santé : à Montélimar, l'ensoleillement provençal rend les ombrières particulièrement productives.",
        points=["Montélimar Agglomération et Drôme provençale", "Ensoleillement très favorable", "Installateur intervenant dans la Drôme et l'Ardèche"],
        contexte="""<h2>Les parkings concernés autour de Montélimar</h2>
<p>Aux portes de la Provence, Montélimar bénéficie d'un ensoleillement élevé. Ses zones commerciales, ses parcs d'activités et les sites industriels de la vallée du Rhône disposent de parkings souvent supérieurs à 1 500 m², pour lesquels l'obligation de la loi APER s'accompagne d'une forte production d'électricité.</p>""",
        sites=["Les <strong>zones commerciales</strong> du nord et du sud de Montélimar.",
               "Les <strong>parcs d'activités</strong> de l'agglomération et des abords de l'A7.",
               "Les <strong>sites industriels et énergétiques</strong> de la vallée du Rhône, jusqu'au Tricastin.",
               "Le <strong>centre hospitalier</strong> et les équipements publics."],
        local="""<h2>Les spécificités d'un projet dans le sud de la Drôme</h2>
<ul>
<li><strong>Mistral :</strong> les vents violents du couloir rhodanien imposent un dimensionnement rigoureux de la structure et des fondations.</li>
<li><strong>Chaleur :</strong> l'ombrage est très apprécié en été, par les clients comme par les salariés.</li>
<li><strong>Production :</strong> le fort ensoleillement améliore le rendement des installations.</li>
<li><strong>Sites sensibles :</strong> autour des sites industriels et énergétiques, les règles d'accès et de sécurité organisent le chantier.</li>
</ul>""",
        faq=[("Le mistral est-il compatible avec des ombrières ?", "Oui, à condition que la structure et les fondations soient dimensionnées pour la zone de vent de votre site. Cela peut renforcer la structure et donc influer sur le budget."),
             ("Une ombrière produit-elle plus à Montélimar ?", "À installation égale, la production est généralement plus élevée que dans le nord de la région grâce au meilleur ensoleillement. La rentabilité dépend aussi du coût de la structure et du mode de valorisation."),
             ("Quelles communes couvrez-vous autour de Montélimar ?", "Montélimar, Pierrelatte, Donzère, Le Teil, Saint-Paul-Trois-Châteaux et la Drôme provençale. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['valence', 'avignon', 'grenoble', 'vienne'],
    ),
    dict(
        slug='besancon', groupe='ville2', nom='Besançon', a='à Besançon', dept='Doubs (25)', cp='25000',
        title="Ombrière Solaire Besançon : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Besançon et dans le Doubs : zones commerciales, microtechniques, neige, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Besançon et dans le Doubs</em>",
        sub="Zones commerciales, technopole et sites industriels, CHU et campus : à Besançon, les grands parkings doivent se préparer à la loi APER en tenant compte d'un climat plus rude.",
        points=["Grand Besançon Métropole", "Industrie et microtechniques", "Installateur intervenant en Franche-Comté"],
        contexte="""<h2>Les parkings concernés autour de Besançon</h2>
<p>Capitale des microtechniques et de l'horlogerie, Besançon accueille des sites industriels de pointe, des zones commerciales de périphérie, un CHU et un campus universitaire. Leurs parkings extérieurs dépassent souvent 1 500 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> de Châteaufarine et des entrées de l'agglomération.",
               "La <strong>technopole</strong> et les sites industriels des microtechniques.",
               "Le <strong>CHU</strong>, les cliniques et le <strong>campus universitaire</strong>.",
               "Les <strong>parcs d'activités</strong> de la métropole."],
        local="""<h2>Les spécificités d'un projet dans le Doubs</h2>
<ul>
<li><strong>Climat :</strong> hivers froids et enneigés : les charges de neige sont intégrées au dimensionnement de la structure.</li>
<li><strong>Production :</strong> l'ensoleillement est plus modéré qu'au sud de Lyon, ce que l'étude de production prend en compte pour comparer les modes de valorisation.</li>
<li><strong>Patrimoine :</strong> la citadelle et les fortifications de Vauban sont inscrites à l'UNESCO : les sites proches demandent une insertion soignée.</li>
<li><strong>Relief :</strong> les parkings en pente ou en terrasses des collines bisontines demandent une structure adaptée.</li>
</ul>""",
        faq=[("Une ombrière est-elle intéressante avec moins de soleil ?", "Oui. L'obligation s'applique quel que soit l'ensoleillement, et la production reste significative. Le choix entre autoconsommation et vente se fait à partir de l'estimation de production propre à votre site."),
             ("La neige pose-t-elle problème ?", "Non, si la structure est dimensionnée pour les charges de neige de votre zone. Il faut aussi prévoir où tombe la neige, pour ne pas gêner le déneigement du parking."),
             ("Quelles communes couvrez-vous dans le Doubs ?", "Besançon, École-Valentin, Chalezeule, Pirey, Montbéliard et le reste du Doubs. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['dijon', 'chalon-sur-saone', 'annemasse', 'bourg-en-bresse'],
    ),
    dict(
        slug='avignon', groupe='ville2', nom='Avignon', a='à Avignon', dept='Vaucluse (84)', cp='84000',
        title="Ombrière Solaire Avignon : Parkings et Loi APER",
        desc="Ombrières photovoltaïques pour parkings à Avignon et dans le Vaucluse : fort ensoleillement, mistral, zones commerciales, loi APER. Étude gratuite.",
        h1="Ombrières solaires de parking <em>à Avignon et dans le Vaucluse</em>",
        sub="Zones commerciales, technopole, plateformes logistiques et agroalimentaires : dans le Grand Avignon, les grands parkings combinent obligation de la loi APER et ensoleillement exceptionnel.",
        points=["Grand Avignon et Vaucluse", "Un ensoleillement parmi les meilleurs de France", "Installateur intervenant dans le Vaucluse et le Gard"],
        contexte="""<h2>Les parkings concernés autour d'Avignon</h2>
<p>Avec l'un des meilleurs ensoleillements de France, le Grand Avignon est un territoire idéal pour les ombrières photovoltaïques. Ses zones commerciales, ses parcs d'activités et ses sites logistiques et agroalimentaires comptent de nombreux parkings de plus de 1 500 m².</p>""",
        sites=["Les <strong>zones commerciales</strong> d'Avignon Nord au Pontet et du sud de l'agglomération.",
               "La <strong>technopole Agroparc</strong> et les zones d'activités de Courtine.",
               "Les <strong>plateformes logistiques et agroalimentaires</strong> du Vaucluse.",
               "Le <strong>centre hospitalier</strong>, le campus et les parkings relais."],
        local="""<h2>Les spécificités d'un projet dans le Vaucluse</h2>
<ul>
<li><strong>Mistral :</strong> les rafales du mistral imposent un dimensionnement rigoureux des structures et des fondations.</li>
<li><strong>Inondations :</strong> les zones proches du Rhône et de la Durance peuvent être soumises à des plans de prévention des risques d'inondation.</li>
<li><strong>Patrimoine :</strong> autour du centre historique inscrit à l'UNESCO, l'avis de l'architecte des Bâtiments de France peut être requis.</li>
<li><strong>Chaleur :</strong> en été, l'ombrage des places est un vrai service pour les clients et les salariés.</li>
</ul>""",
        faq=[("Une ombrière est-elle très rentable à Avignon ?", "À installation égale, la production y est parmi les plus élevées de France. La rentabilité dépend aussi du coût de la structure, renforcée face au mistral, du raccordement et du mode de valorisation : seule l'étude permet de chiffrer."),
             ("Faut-il tenir compte du risque d'inondation ?", "Oui, si le parking se trouve dans une zone couverte par un plan de prévention des risques. Il encadre la conception des structures et la position des équipements électriques."),
             ("Quelles communes couvrez-vous autour d'Avignon ?", "Avignon, Le Pontet, Sorgues, Vedène, Cavaillon, Carpentras, Orange et les communes voisines du Gard. Indiquez le code postal du parking dans le formulaire.")],
        voisins=['montelimar', 'valence', 'lyon', 'grenoble'],
    ),
]

PAR_SLUG = {v['slug']: v for v in VILLES}
HUB = '/zones-intervention'


def path(v):
    return f"/ombriere-solaire-{v['slug']}"


def all_paths():
    return [HUB] + [path(v) for v in VILLES]


def local_links(v):
    cards = ''.join(f'<a href="{path(PAR_SLUG[s])}" class="link-card">Ombrières solaires {esc(PAR_SLUG[s]["a"])}</a>' for s in v['voisins'])
    cards += f'<a href="{HUB}" class="link-card">Toutes nos zones d\'intervention</a>'
    guides = ''.join(f'<a href="{u}" class="link-card">{esc(t)}</a>' for u, t in [
        ('/obligation-ombriere-parking', "Obligation loi APER : parkings concernés, échéances"),
        ('/financement-ombriere-solaire', "Financer une ombrière : achat, tiers-investissement, location"),
        ('/devis-ombriere-solaire', "Demander une étude gratuite")])
    return (f'<section class="links"><div class="wrap"><h3>Près de chez vous</h3><div class="links-grid">{cards}</div>'
            f'<h3 style="margin-top:2rem">Nos guides</h3><div class="links-grid">{guides}</div></div></section>\n')


def page_ville(v):
    p = path(v)
    sites = ''.join(f'<li>{s}</li>' for s in v['sites'])
    preselect = 'Entreprise / site industriel' if v['groupe'] == 'pole' else None
    main = hero(f"{esc(v['dept'])} · étude gratuite", v['h1'], v['sub'], v['points'],
                f"Ombrière solaire — page {v['nom']}", preselect=preselect)
    main = main.replace('placeholder="Ex : 69007"', f'placeholder="Ex : {v["cp"]}"')
    main += f'''<article class="content">
{v['contexte']}
<h3>Les types de sites les plus souvent concernés</h3>
<ul>
{sites}
</ul>
{v['local']}
<h2>L'obligation et ses échéances, {esc(v['a'])} comme ailleurs</h2>
<p>La loi APER impose d'équiper d'ombrières photovoltaïques au moins la moitié de la surface des parkings extérieurs non concédés de plus de 1 500 m². L'échéance est fixée au 1<sup>er</sup> juillet 2026 au-delà de 10 000 m² et au 1<sup>er</sup> juillet 2028 entre 1 500 et 10 000 m², avec des délais possibles sous conditions. Le détail est dans notre <a href="/obligation-ombriere-parking">guide de la loi APER</a> ; les modes de financement sont comparés sur notre page <a href="/financement-ombriere-solaire">financement</a>.</p>
<h2>Comment se passe l'étude {esc(v['a'])} ?</h2>
<p>Vous décrivez votre parking dans le formulaire. Un installateur partenaire qui intervient dans votre secteur ({esc(v['dept'])}) vous rappelle sous 48&nbsp;h ouvrées, vérifie la surface concernée et vos échéances, puis vous propose, si le projet est pertinent, une étude de faisabilité : implantation, production estimée, raccordement, autorisations et financement. L'étude est gratuite et sans engagement.</p>
{cta_row()}
</article>
'''
    main += faq(v['faq'])
    main += local_links(v)
    main += final(f"Votre parking {esc(v['a'])} est concerné ?")
    extra = {'@type': 'Service', 'name': f"Étude d'ombrières photovoltaïques de parking {v['a']}",
             'serviceType': 'Ombrières photovoltaïques de parking', 'provider': {'@id': pages.ORG_ID},
             'areaServed': {'@type': 'Place' if v['groupe'] == 'pole' else 'City', 'name': v['nom']}}
    write(p, v['title'], v['desc'], main, crumb=f"Ombrières {v['nom']}", faqs=v['faq'], extra=extra)


def page_hub():
    def cards(groupe):
        return ''.join(
            f'<a href="{path(v)}" class="card"><span class="card-ic">{pages.ic("map")}</span><h3>{esc(v["nom"])}</h3>'
            f'<p>{esc(v["dept"])}</p><span class="more">Voir la page →</span></a>'
            for v in VILLES if v['groupe'] == groupe)
    hub_faq = [
        ("Intervenez-vous en dehors de ces villes ?", "Oui. Ces pages présentent nos principaux secteurs, mais nos installateurs partenaires interviennent plus largement en Auvergne-Rhône-Alpes et dans les départements voisins. Indiquez le code postal de votre parking dans le formulaire."),
        ("Qui réalise l'étude ?", "Un installateur partenaire qui intervient dans votre département. Il vous rappelle sous 48 heures ouvrées pour un premier échange, puis organise l'étude si le projet est pertinent."),
        ("L'étude est-elle payante ?", "Non. L'étude et les échanges sont gratuits et sans engagement."),
    ]
    main = hero("Lyon et Auvergne-Rhône-Alpes · étude gratuite",
                "Ombrières solaires de parking <em>autour de Lyon</em>",
                "Nos installateurs partenaires interviennent dans un rayon d'environ trois heures autour de Lyon : Auvergne-Rhône-Alpes, Bourgogne-Franche-Comté et nord du Vaucluse. Choisissez votre secteur ou décrivez directement votre parking.",
                ["Métropoles et villes moyennes", "Grands pôles logistiques et industriels", "Un installateur proche de votre site"],
                "Ombrière solaire — page zones d'intervention")
    main += f'''<section class="section">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Villes</span><h2>Nos principales villes d'intervention</h2><p>Chaque page présente les sites concernés et les contraintes locales : climat, urbanisme, paysage.</p></div>
    <div class="cards">{cards('ville')}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Villes moyennes</span><h2>Les autres villes où nous intervenons</h2><p>Des agglomérations aux zones d'activités importantes, de la Saône à la vallée du Rhône et aux portes de Genève.</p></div>
    <div class="cards">{cards('ville2')}</div>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="s-head"><span class="kicker">Pôles d'activités</span><h2>Les grands pôles logistiques et industriels</h2><p>C'est là que se trouvent les parkings les plus vastes, souvent concernés par l'échéance la plus proche.</p></div>
    <div class="cards">{cards('pole')}</div>
    {cta_row()}
  </div>
</section>
'''
    main += faq(hub_faq)
    main += final()
    write(HUB, "Ombrières Solaires autour de Lyon : Zones d'Intervention",
          "Ombrières photovoltaïques de parking à Lyon, Grenoble, Saint-Étienne, Annecy, Chambéry, Clermont-Ferrand, Dijon, Valence et pôles logistiques.",
          main, crumb="Zones d'intervention", faqs=hub_faq)


def build():
    for v in VILLES:
        page_ville(v)
    page_hub()
    print(f'{len(VILLES)} pages locales et la page {HUB} générées.')


if __name__ == '__main__':
    build()
