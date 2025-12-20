# from genshin_calculator import team
from genshin_calculator.artifacts import ARTIFACTS
from genshin_calculator.build import Build
from genshin_calculator.calculator import Calculator
from genshin_calculator.characters import Wanderer
from genshin_calculator.rotation import Rotation
from genshin_calculator.stats import STATS, DmgType, ElementType 
from genshin_calculator.weapons import CATALYST


BENNETT = Build(STATS.ATK(1.19 * 756), # Bennet Ult
                STATS.ATK_PERC(20 + 30), # Noble + Wanderer A4
                )
FARUZAN = Build(STATS.EM(100), STATS.ATK(20), # Elegy
                STATS.DMG(38.3, ElementType.ANEMO), STATS.RES_SHRED(30, ElementType.ANEMO), # Ult
                STATS.FLAT_DMG(0.32 * 805, ElementType.ANEMO), # A5
                STATS.CRIT_DMG(40, ElementType.ANEMO) # C6
                )

ZHONGLI = Build(STATS.RES_SHRED(20),
                STATS.ATK_PERC(20), #Millelithe
                STATS.DMG(12), # Cinder City
                name="Zhongli",
                )

YANFEI1 = Build(STATS.ATK_PERC(48), # Dragon tale
                STATS.ATK_PERC(20), #Millelithe
                STATS.ATK_PERC(25), # Pyro resonnance
                name="Yanfei_milellithe",
                )

YANFEI2 = Build(STATS.ATK_PERC(48), # Dragon tale
                STATS.DMG(12), # Cinder City
                STATS.ATK_PERC(25), # Pyro resonnance
                name="Yanfei_cindercity",
                )

LANYAN = Build(STATS.ATK_PERC(48), # Dragon tale
               STATS.ATK_PERC(20), #Millelithe
               STATS.DMG(12), # Cinder City
               name="LanYan")

CITLALI1 = Build(STATS.DMG(28), # Weapon
                STATS.ATK_PERC(20), #Millelithe
                STATS.DMG(12), # Cinder City
                STATS.FLAT_DMG(2 * 822 * 0.6),
                name="Citlali_C1")

CITLALI2 = Build(STATS.DMG(28), # Weapon
                 STATS.ATK_PERC(20), #Millelithe
                 STATS.DMG(12), # Cinder City
                 STATS.CRIT_RATE(20),
                 name="Citlali_cryo")

DURIN1 = Build(STATS.RES_SHRED(20),
               STATS.DMG(12), # Cinder City
               STATS.ATK_PERC(25), # Pyro resonnance
               name="Durin_cindercity")

DURIN2 = Build(STATS.RES_SHRED(20),
               STATS.ATK_PERC(20), #Millelithe
               STATS.ATK_PERC(25), # Pyro resonnance
               name="Durin_millelithe")

THOMAS1 = Build(STATS.DMG(15),
                STATS.ATK_PERC(20), #Millelithe
                STATS.ATK_PERC(25), # Pyro resonnance
                name="Thomas_millelithe")

THOMAS2 = Build(STATS.DMG(15),
                STATS.DMG(12), # Cinder City
                STATS.ATK_PERC(25), # Pyro resonnance
                name="Thomas_cindercity")

IFA = Build(STATS.ATK_PERC(48), # Dragon tale
            STATS.ATK_PERC(20), #Millelithe
            STATS.DMG(40), # Cinder City
            name="Ifa")



calculator = Calculator(weapons=[CATALYST.FOUR_WINDS(refinement=3),
                                 CATALYST.WIDSITH(refinement=5)
                                 ], # function get_all ? ou BOW.retrieve()
                        flowers=[ARTIFACTS.DESERT_PAVILION(STATS.FLAT_HP(4780),
                                                           STATS.FLAT_ATK(19),
                                                           STATS.CRIT_RATE(15.2),
                                                           STATS.EM(23),
                                                           STATS.ATK_PERC(11.7)),
                                 ARTIFACTS.DESERT_PAVILION(STATS.CRIT_RATE(12.4),
                                                           STATS.CRIT_DMG(5.4),
                                                           STATS.ATK_PERC(4.1),
                                                           STATS.EM(44))
                                                           ],
                        feathers=[ARTIFACTS.DESERT_PAVILION(STATS.FLAT_ATK(311),
                                                            STATS.CRIT_RATE(6.6),
                                                            STATS.EM(23),
                                                            STATS.ATK_PERC(5.8),
                                                            STATS.CRIT_DMG(26.4))],
                        sands=[ARTIFACTS.DESERT_PAVILION(STATS.ATK_PERC(46.6),
                                                         STATS.FLAT_ATK(35),
                                                         STATS.DEF_PERC(21.1),
                                                         STATS.CRIT_RATE(2.7),
                                                         STATS.CRIT_DMG(19.4)),
                               ARTIFACTS.DESERT_PAVILION(STATS.ATK_PERC(46.6),
                                                         STATS.FLAT_ATK(37),
                                                         STATS.CRIT_RATE(7.8),
                                                         STATS.CRIT_DMG(7.8))
                                                         ],
                        cups=[ARTIFACTS.RANDOM_ARTIFACT(STATS.DMG(46.6, ElementType.ANEMO),
                                                        STATS.CRIT_RATE(7.4),
                                                        STATS.CRIT_DMG(20.2),
                                                        STATS.ATK_PERC(9.9),
                                                        STATS.FLAT_HP(209))],
                        helmets=[ARTIFACTS.DESERT_PAVILION(STATS.CRIT_DMG(62.2),
                                                           STATS.DEF_PERC(20.4),
                                                           STATS.ATK_PERC(10.5),
                                                           STATS.FLAT_HP(239),
                                                           STATS.FLAT_ATK(31)),
                                 ARTIFACTS.DESERT_PAVILION(STATS.CRIT_DMG(62.2),
                                                           STATS.CRIT_RATE(6.6),
                                                           STATS.EM(23)),
                                 ARTIFACTS.DESERT_PAVILION(STATS.CRIT_RATE(31.1),
                                                           STATS.ER(16.2),
                                                           STATS.EM(21),
                                                           STATS.CRIT_DMG(13.2)),
                                                           ],
                        team_bonuses=[BENNETT + FARUZAN + ZHONGLI,
                                      BENNETT + FARUZAN + CITLALI1,
                                      BENNETT + FARUZAN + CITLALI2,
                                      BENNETT + FARUZAN + LANYAN,
                                      BENNETT + FARUZAN + YANFEI1,
                                      BENNETT + FARUZAN + YANFEI2,
                                      BENNETT + FARUZAN + DURIN1,
                                      BENNETT + FARUZAN + DURIN2,
                                      BENNETT + FARUZAN + THOMAS1,
                                      BENNETT + FARUZAN + THOMAS2,
                                      BENNETT + FARUZAN + IFA,
                                       ], 
                        )


results = []
for build in calculator:
      wanderer = Wanderer(weapons=build.weapons,
                          flowers=build.flowers,
                          feathers=build.feathers,
                          sands=build.sands,
                          cups=build.cups,
                          helmets=build.helmets,
                          team_bonuses=build.team_bonuses)
      
      rotation = Rotation(wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.358),
                          wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.285),
                          wanderer.attack(DmgType.CHARGED, ElementType.ANEMO, 1.43 * 2.377))
      damage = rotation.compute(resistances=30, ennemy_lvl=90)
      
      
      # rotation = Rotation(wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.358),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.285),
      #                     wanderer.attack(DmgType.CHARGED, ElementType.ANEMO, 1.43 * 2.377),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.358),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.285),
      #                     wanderer.attack(DmgType.CHARGED, ElementType.ANEMO, 1.43 * 2.377))
      # damage = rotation.compute(resistances=30, ennemy_lvl=90)

      # wanderer.weapons += Build(STATS.DMG(12))
      # rotation = Rotation(wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.358),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.285),
      #                     wanderer.attack(DmgType.CHARGED, ElementType.ANEMO, 1.43 * 2.377),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.358),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.285),
      #                     wanderer.attack(DmgType.CHARGED, ElementType.ANEMO, 1.43 * 2.377))
      # damage += rotation.compute(resistances=30, ennemy_lvl=90)

      # wanderer.weapons += Build(STATS.DMG(12))
      # rotation = Rotation(wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.358),
      #                     wanderer.attack(DmgType.NORMAL, ElementType.ANEMO, 1.537 * 1.285),
      #                     wanderer.attack(DmgType.CHARGED, ElementType.ANEMO, 1.43 * 2.377))
      # damage += rotation.compute(resistances=30, ennemy_lvl=90)

      results.append((round(sum(damage)), [round(d) for d in damage], build.name))

for result in sorted(results, key=lambda elem: elem[0]):
      print(*result)




