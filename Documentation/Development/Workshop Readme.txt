
                                        HISTORY OF CHANGES


##############################################################################################
                                           Version 0.14
                                         Released - 3/10/13
##############################################################################################
* Bug Fixes:
   ---  Map travel has been slowed down to the native speed.
   ---  Battle continuation should now be working properly in the field.
   ---  Debug message spam that disables the message log should no longer occur.
   ---  Health regeneration should be functioning as intended now.
   ---  Nissa Part I quest should no longer spawn a list of script errors when talking to the 
        elder upon arrival.
   ---  Nissa Part II quest should properly load contestants to fight.
   ---  Nissa Part II quest should now trigger her dialog instead of an empty string.
   ---  Books added in v0.12 will now be readable by the player via the camp menu.
   ---  Fire arrows now work again.

* Appearance:
   ---  All travelers, minstrels, book merchants and ransom brokers have unique names.

* Conveniences:
   ---  You now have a "never mind" option to escape out of the "I'd like to ask you 
        something" option during a companion conversation.
   ---  A mod option has been added to enable / disable the troop ratio bar in combat.
   ---  A mod option has been added to enable / disable troop prefixes similar to the ones 
        used in the Floris Mod Pack.
   ---  Travelers can now be paid to tell you were minstrels, ransom brokers and book 
        merchants are located.
   ---  Companions may now have their character history exported and imported.

* Quest Pack 5: Village Quests
   ---  New Quest (villages): Sending Aid.



##############################################################################################
                                           Version 0.13
                                         Released - 3/2/13
##############################################################################################
* Bug Fixes:
   ---  Defeated patrols will no longer display a host of script errors, but will be cleaned 
        out when you try to access information about them.
   ---  The list of troops for setting upgrade paths while speaking to the Captain of the 
        Guard will now display if you're using a faction that isn't the custom player faction.
   ---  When you withdraw money from the treasury you'll now receive it.  Novel, huh?
   ---  AI heroes will now appropriately upgrade their village improvements.
   ---  The diplomacy in-game guide now has a credits page.
   ---  Sending Nissa on a mission to support you as king should no longer cause repeated 
        errors due to a non-existent rival wanting to object.
   ---  The "show all items" screen should no longer show the "Invalid Item".
   ---  Numerous heraldic items were worth only 1 denar and now have more realistic values.
   ---  Recruiting from villages during mandatory conscription should no longer cause DIV / 0 
        errors and should no longer cost you money.
   ---  When summoned to your hall by a steward the quest shouldn't fail to continue on to 
        the reason you were summoned for.  (Failed npc_map_talk_context).
   ---  Replacing an advisor when none is currently assigned should no longer result in 
        script errors.

* Game Balancing:
   ---  The price of salt is now cheaper at the salt mine.
   ---  Advisors may now be appointed by speaking to a companion directly.  This allows you 
        to appoint them as a vassal instead of being a king.
   ---  Indicted lords have their controversy reset to prevent the being stuck in a 
        controversial loop.  (Credit: Zsar)

* Conveniences:
   ---  The game option for bodyguards is now a menu that allows limiting them to a number 
        between 1 and 4 or disabling them entirely.
   ---  The trade ledger can be accessed from the town marketplace and personal reports menus 
        once you have assessed local prices at least once.

* Appearance:
   ---  A new regional name generator has been added.  This allows every NPC, permanent or 
        quest related, to be dynamically named based upon the culture they're from.  Each 
        NPC has now been given unique names.
   ---  Several new mercenary company names have been added.

* New Option: Mod Difficulty:
   ---  A new "mod difficulty" option has been added to the character creation process that 
        alters a number of features designed at making the mod "easy", "normal", "hard" or 
        "very hard".  The default setting is normal.
   ---  The game difficulty setting found in the mod options has been removed.
   ---  Mod Difficulty now alters:
         ---  The size of AI parties.
         ---  The size and composition of initial garrisons for castles and towns.
         ---  The strength of troops AI parties use to rebuild their party.
         ---  The maximum number of bandit and deserter parties that spawn on the map.

* Book Improvements:
   ---  Added 5 new standard readable books for tracking, training, first-aid, prisoner 
        management and charisma.
   ---  Added 2 new specialty readable books.
   ---  Added 1 new standard reference book for path-finding.
   ---  Standardized the cost of all books based on the benefit type they give.
   ---  Readable books now display what they do in their tooltip.
   ---  Book merchants now have their inventory re-shuffled when they change locations.

* Village Quest System:
   ---  Village quests no longer have quest-based cooldowns.  Instead they are gated by 
        village-based cooldowns.  Quest A may be completed in Village A and then 
        immediately started in Village B, but Village A won't have any quests available 
        again for a few days.
   ---  New Quest (villages): A Craftsman's Knowledge.

* Included Mods:
   ---  Trade Ledger by Caba'drin.  Adds a new "personal report" presentation for tracking 
        trade values in towns whenever you assess prices.
   ---  Dynamic Arrays by Sphere.  More of an under the hood addition to support the trade 
        ledger, but added for my notes.
   ---  Cinematic Compilation by DOMA.   Adds a number of graphical & sound improvements.  
        Only included on the "cinematic download" copy.
   ---  Ethnic Troops by Nemchenk.  More racially diverse facial codes.

* Removed Mods:
   ---  Quest Pack 2 (Trade Quests).  For those who may have discovered these they were not 
        ready for release yet and should have been blocked from triggering.


##############################################################################################
                                           Version 0.12
                                         Released 2/13/13
##############################################################################################
* Bug Fixes:
   ---  Your quartermaster shouldn't ninja sell books you give him now.
   ---  Party emoticons should actually be disabled now and stay that way.

* Conveniences:
   ---  You can now turn in partial prisoner amounts in quest "Capture Prisoners".

##############################################################################################
                                           Version 0.11
                                         Released 2/12/13
##############################################################################################
* Bug Fixes:
   ---  Fixed inaccurate key command names from being displayed within the key config 
        screen and during troop deployment.
   ---  Lords that have defected to your kingdom will not be affected by your weekly 
        relation changes until accepted as a vassal.
   ---  The garrison training troop selection list shouldn't spawn invalid troop errors 
        when using a custom culture now.
   ---  Disabled Emoticons due to occasional crash-to-desktop issues.
   ---  Removing an appointed castle steward now cancels any associated quest given by 
        that steward with the exception of the mercenary contract.
   ---  Quest "Raise Troops" should no longer assign "veteran fighters" as a goal.
   ---  When troop tiers are displayed they should no longer account for upgrading bandits.
   ---  Deserters shouldn't have naked veteran fighters within them any longer.

* Conveniences:
   ---  New game option added to prevent "pop-up" notifications.
   ---  Game option for pausing fast travel refined into a pop-up menu to select between 
        "Any Enemies" (current functionality) and "Actual Threats" (only pauses for enemy 
        heroes, hostile groups as large as your own or anyone actively seeking to attack you).
   ---  Fast travel should now pause if a party related to an active quest is near at 
        any setting.

* Game Balancing:
   ---  No fief relation percentage penalty reduced from -75% to 0%.
   ---  Quest "Raise Troops" requires troops to be upgraded a little less than native now.

* Center Improvements:
   ---  New Improvement: Training Grounds (castles, towns) improves the chance of troops 
        upgrading to the next tier during Captain of the Guard training by 5% and reduces 
        the cost of garrison training by 10%.

* Book Improvements:
   ---  Reading speed is now directly set by character intelligence.  (14 INT = native speed)
   ---  Companions can now be assigned to read books in their inventory via the 
        companion management menu options.
   ---  Advisors can be given books and will read at a slower pace when not in your party.


##############################################################################################
                                           Version 0.10
                                         Released 2/10/13
##############################################################################################
* Bug Fixes:
   ---  Nissa should give a proper final comment after completing her story arc.
   ---  The slaver availability setting in kingdom management should now work properly.
   ---  The "restore defaults" button in the game options now works.
   ---  Morale changes for other parties should not display anymore.
   ---  After combat you will always be directed to the autoloot menu even if no companion 
        has this enabled to allow for quartermasters to pick up loot.
   ---  A companion kicked out of the party will perform any companion role turnover to 
        the player as needed.
   ---  Fixed several tooltips within the kingdom management report.
   ---  The weekly budget no longer refers to your party using random party names.
   ---  Tournaments should no longer occasionally have looping noises stuck playing.
   ---  When companions quit they will be removed from any party roles now.
   ---  Lord holdings screen should no longer show % relation changes if you aren't ruler.

* Conveniences:
   ---  Prisoner caravans no longer show on the weekly budget unless one is active.
   ---  Added option to pause fast travel when enemies are near.  (Credit: Caba'drin).
   ---  PBOD preferences have been merged into the main game options screen.
   ---  Your minister now has an option to let you drop ownership of a fief.
   ---  Post combat debrief now displays kill counts by "heroes".  (Credit: Custom Commander)
   ---  You can now ask an advisor to see their character screen.
   ---  When asking a lord or lady for the location of someone, they will note their relatives.

* Appearance:
   ---  Altered the appearance of the game mod options order & added title bars.
   ---  Weekly budget altered so that it is easier to read the numbers.

* Game Balancing:
   ---  Advisors now gain 10 renown & 250xp each week while holding office.
   ---  Requesting your Castle Steward to host a tournament costs 8000 denars now.
   ---  Hosting a tournament via the Castle Steward improves town relation by 3.
   ---  Normal tournament spear speed increased from 85 to 95.
   ---  Enhanced tournament spear speed increased from 85 to 90.

* New Advisor: Captain of the Guard
   ---  Allows a companion to be appointed in any castle or town to handle regional patrols,
        garrison recruitment, garrison training and the associated aspects of the treasury.

* New System: Regional Patrols
   ---  Up to 3 patrols may be petitioned per keep to guard the area around their home.
   ---  Patrols are managed within the weekly budget and are disbanded if not paid.
   ---  Patrols can be ordered to turnover any prisoners they have to their owning lord.
   ---  The owner of a patrol can order them to follow their lord or defend a different fief.
   ---  If the Captain of the Guard is removed then every patrol attached to him is disbanded.
   ---  Kingdom policies that alter troop wages are twice as effective with patrols.
   ---  Patrols will join allied parties in combat if nearby.

* New System: Garrison Recruitment
   ---  Each village contributes recruits to their associated castle or town based on a number
        of circumstances ranging from prosperity, player renown, captain of the guard renown
        and persuasion, distance from its associated town, kingdom policies and game difficulty.
   ---  Each town will also contribute to its own recruitment using the same factors.
   ---  The cost for recruitment is on a per recruit basis and is funded by the castle treasury.
   ---  The Captain of the Guard will recruit a garrison up to a size limited by the
        combination of his leadership & persuasion skills.

* New System: Garrison Training
   ---  Each castle or town with a Captain of the Guard stationed there can be set to
        automatically train recruits causing them to upgrade to the next tier.
   ---  The percentage of recruits that upgrade is dependant upon a combination of the 
        Captain of the Guard's leadership & training skills.
   ---  The cost for training is on a per upgrade basis and is funded by the castle treasury.

* New System: Treasury
   ---  Each castle or town can establish a treasury to fund options related to its defense.
   ---  A treasury allows direct deposits or withdrawals via the Captain of the Guard.
   ---  A treasury can have an income allocated to it on a per weekly basis so that it will
        not be necessary to keep making deposits to keep it funded.


##############################################################################################
                                           Version 0.09
                                         Released 1/24/13
##############################################################################################
* Bug Fixes:
   ---  Companion advisors should now display properly in the companion mission report.
   ---  Storekeepers will now auto-buy food when leaving a fief if so configured.
   ---  The storekeeper's description text in the "assign party roles" screen now properly 
        displays the food variety morale bonus when using the alternate morale system.
   ---  Hired mercenary parties now build their party based upon their named culture, not 
        the one of the city they were spawned within.  
        Note: As a result the mercenary parties will go through some odd changes for a week.
   ---  Renewing a contract with a hired mercenary party should no longer lock up the game.
   ---  Hired mercenary parties should now attempt to replenish their numbers with recruits.
   ---  Hired mercenary parties should now attempt to upgrade their troops every 14 days.
   ---  Mercenary parties will now expect payment weekly after renewing their contract.  
        Previously this was not occurring.

* Game Balancing:
   ---  Staying within a city grants a 33% chance of reducing march penalty by 1 every 6 hours.
   ---  Hired mercenary parties will now attempt to upgrade their troops every 14 days 
        down from 30 days.
   ---  Characters with persuasion 2 or greater may attempt haggling mercenary party 
        costs down by 15% when it comes time to renew their contract.

* Conveniences:
   ---  Center notes now display any improvements built or in construction, any player 
        owned enterprises and description on how the center views the player.
   ---  The "View Lord Holdings" presentation has been changed as follows:
         ---  A lord's renown value is now displayed under their name.
         ---  A lord's reputation type is now displayed under their name if previously met 
              or the lord is a vassal under the player.
         ---  The initial faction displayed upon opening should always be the player's.
   ---  Morale changes are now displayed on the message log in green or red coloring.

* Center Improvements:
   ---  Raiding or besieging parties now have a 0.5% chance per point of looting of 
        dealing double damage to an improvement.  Lords begin with a 2% chance with 
        certain lords gaining bonuses based upon their reputation type in addition to 
        their looting skill.

* Enhanced Diplomacy:
   ---  Vassals are now given a boost to weekly relation gain based upon fiefs owned.  
        If no fiefs are owned by a vassal then it becomes a penalty.
         ---  +30% for each village.
         ---  +55% for each castle.
         ---  +75% for each town.
         ---  -50% for having no fiefs.
   ---  New game option added to force vassals, with the player as ruler, to reinforce 
        their party with troops from the player's chosen culture vs. their original one.


##############################################################################################
                                           Version 0.08
                                         Released 1/21/13
##############################################################################################
* Bug Fixes:
   ---  Scene exits within towns should work properly instead of displaying a ".".
   ---  Fixed division by zero errors from diplomacy_get_player_party_morale_values 
        when switching from native morale system to the alternate one.
   ---  The salt mine now enters into its own town menu instead of the last town visited.

* Conveniences:
   ---  Companion inventories can now be directly accessed from the town marketplace.  No 
        really, I'm not kidding this time.

* Game Balancing:
   ---  Disabled castle garrison patrols until the Captain of the Guard feature is 
        introduced giving it more control options for players.


##############################################################################################
                                           Version 0.07
                                         Released 1/17/13
##############################################################################################
* Bug Fixes:
   ---  PBOD menus should now show the proper 'F#' values.
   ---  Accessing a companion's inventory menu is limited to the first 11 companions unless 
        they are one of your party roles to prevent being stuck in that menu.
   ---  Raiding villages should no longer yield only butter at times.

* Conveniences:
   ---  Companions that are turned into vassals will no longer have their equipment replaced.
   ---  The native banner presentation now has a "previous page" button.
   ---  The tournament in-game guide has been added to the "Reference Material" menu.
   ---  A new Diplomacy in-game guide has been added to the "Reference Material" menu.
   ---  You only need to go through the introduction for ransom brokers once now.
   ---  Companion inventories can be directly accessed from the town marketplace.

* Game Balancing:
   ---  AI opponents during "elimination mode" tournaments have been buffed slightly, but 
        still remain a little easier than "performance mode" opponents.
   ---  Party unity range extended from -30/+30 to -40/+40.
   ---  Upon being made a vassal companions retain any current renown they built up from 
        tournaments and their maximum starting renown has been improved from 200 to 400.
   ---  Hero escape chance from the player party has been increased from 5% to 15%.
   ---  Hero escape chance from the player party is reduced by 1.3% per point of prisoner 
        management.
   ---  Time before a lord without a party will respawn has been increased from 48 to 96 hours.

* Appearance:
   ---  Fixed the background color for dozens of banners .  Still more to go.
   ---  Moved PBOD's split party assignments to the "Party Reports" menu.

* Kingdom Policies & Decrees:
   ---  Once you are a king you may alter the domestic policies of your kingdom which 
        have many effects on your kingdom in the long term.  You may also enact royal 
        decrees that are meant as a temporary measure based upon the needs of your kingdom.
   ---  AI kingdoms will have their own policy settings which should make being a vassal 
        in each kingdom a slightly different experience.
   ---  As a vassal you may view the policy screen for your kingdom, but cannot alter it.
   ---  The kingdom policies can be accessed via reports -> kingdom reports -> kingdom 
        management.

* Companions:
   ---  New Companion - Nissa.  This is taken directly from the Odval companion of Floris 
        created by Monnikje.  I wanted to have her in the game so that her story arc quest 
        chain could be tested without having her directly identical to Odval as I'll 
        likely make changes along the way.
   ---  Added new morality type: "egotistic".
   ---  Added new morality type: "gladiator"

* Quests:
   ---  New quest chain - Nissa's Redemption.  This adds 5 quests to the game along with 
        a new feature of 'permanent loyalty' if you complete the entire story arc 
        successfully on the hard quest setting.

* Included Mods:
   ---  Emoticons by Lav.  Adds rotating icons displaying AI behavior on the map.  This 
        can be disabled in the main mod options.


##############################################################################################
                                           Version 0.06
                                         Released 7/20/12
##############################################################################################
* Party Morale:
   ---  New Mechanic: "Party Unity"
         ---  + [ (combined leadership of all companions & player) * 3 ]
         ---  Companions are ignored as troops.
         ---  -1 for every 3 troops of your faction in your party.
         ---  -1 for every troop not of your faction in your party.
         ---  -2 for every mercenary in your party.
         ---  Value is restricted to -30 to +30.
   ---  Party size benefit to morale is capped at +30.
   ---  Party size benefit improved to +1 per 8 troops.
   ---  Food no longer provides 150% of the listed benefit.  It provides 100%.
   ---  Point of desertion reduced from 31 to 20 morale.

* Center Improvements:
   ---  Mercenary chapterhouses now ensure a minimum level of 19 for mercenaries available.
   ---  Mercenary chapterhouses now reduce the cost of mercenaries by 40% instead of 15%.

* Game Changes:
   ---  The town guild master can now be accessed directly from the town menu.
   ---  Quests from the town guild master may now be accessed via a list of options during 
        dialog with him.
   ---  Brognar's voice acting pack has been removed.

* Bug Fixes:
   ---  Slaughtering all of your cattle in a herd should no longer cause invalid party 
        script errors.
   ---  Accepting or rejecting selling all prisoners to a ransom broker now ends the 
        conversation.
   ---  Quest "Summoned to Hall" should now trigger properly in the intended location.


##############################################################################################
                                           Version 0.05
                                         Released 7/15/12
##############################################################################################
* Center Improvements:
   ---  Bugfix to allow the "Field of Grain" improvement to be built repeatedly.  If you've
        already built one the game will fix itself.
   ---  Bugfix to prevent the "cancel work" menu from showing if no building is in progress.
   ---  New Improvement: Castle Library (castles, towns) grants double reading progress while
        resting in a center with this improvement.

* Companion Role Updates:
   ---  The "gaoler" should now sell things at the ransom broker rate vs. the flat 50 denars.

* Diplomatic Changes:
   ---  Rejecting a ransom offer does not incur an honor penalty while at war.
   ---  Giving troops to one of your vassals will improve your relation with them.
   ---  The starting factional disputes have been altered to even the conflicts out a little.
   ---  Diplomatic Role: "Castle Steward" added that companions can be assigned to.  This is
        still in a very early stage of development, but allows access to building, repairing,
        or cancelling construction on an improvement as well as gives advice on what should
        be focused on next for the castle.  This advisor can be appointed only by your chief
        minister.
   ---  Your chief minister can now change your faction's culture.  It takes 3 days before
        the effects become evident.
   ---  The player's faction now has its own troop tree (which mirrors Swadia for now), but
        can be edited with Morph's editor to make your own troop tree.

* Tournament Changes:
   ---  Updated to version 1.6.
   ---  A new "Hall of record" report was developed to show how you performed in tournaments
        for each city.
   ---  Tournaments now can be run in two different modes set in the main mod options page.
   --- "Elimination Mode" is similar to native design.  You can't set the size or number  
       of teams.  Participants are selected for continuation based upon the following
       priority: survivors, remaining members of the surviving team, members of the
       highest scoring team and then finally the highest scoring participants not
       already selected.
   --- "Performance Mode" is the score based system TPE was originally designed upon.  It
       remains the default mode of play.

* Appearance & Graphics:
   ---  Included: "Custom Clan Banner Pack" by MadocComadrin.
   ---  Added numerous new heraldic armors and replaced some faction armors with them.
   ---  Minor color alterations have been made to the text messages for quest log updates and
        morale changes.
   ---  Faction colors may now be altered once you are a king.

* Reports Menu:
   ---  Revamped the reports menu similar to the way it appeared in Floris 2.5 using a smaller
        list of similarly grouped reports.
   ---  New Report: "Estates of the Realm" (kingdom) has been added.
   ---  New Report: "Show All Items" (reference) from Custom Commander by rubik has been added.
   ---  New Report: "Tournament History" (personal) has been added.

* Party Morale:
   ---  Party size gives a benefit for every 15 men vs. a negative equal to your current size.
   ---  Base party morale has been reduced from 50 to 0.
   ---  Leadership contributes roughly 1/3rd the benefit it previously did.
   ---  New Mechanic: "Days on the March" - The longer you spend away from your homelands on
        the march the more of a morale penalty your army will receive.  This is slowly
        reduced as you spent more time in your own territories.

* Reading Books:
   ---  Books that grant permanent increases should now be readable at any time and still
        allow you to raise a skill as high as your attributes would have allowed without it.


##############################################################################################
                                           Version 0.04
                                         Released 6/26/12
##############################################################################################
* Message Log Filtering:
   ---  Villages being raided should no longer show up in the log unless the village or the 
        raider is of your faction.  If they do show up they should be colored green if your 
        faction does the raiding or red if your faction’s village is being raided.
   ---  Lords being taken prisoner, freed from captivity or defeated and escape it should 
        no longer show up unless they are of your faction.  These messages will be red/green 
        colored based on if this is beneficial to your faction or not.
   ---  Castles and towns under siege should no longer display this unless you are a member 
        of the attacking or defending faction.  Message will be colored red / green as 
        appropriate.
   ---  Lords defecting will no longer appear in the message log unless they are joining or 
        leaving your faction with red/green coloring as appropriate.
   ---  Messages regarding the seizing of a castle or town will show up red or green if your 
        faction is involved or light blue if not.  These messages are not hidden.

* Center Improvements:
   ---  AI lords will now build center improvements on their own if in an owned town and 
        they have enough disposable income (so as to not deplete their army funds).  A 
        scripted priority has been designed so that they’ll try to do so in an intelligent 
        order.
   ---  AI lords will now repair damaged center improvements.  Repairs are given priority 
        over new construction.
   ---  Castle and town improvements are now damaged upon a successful siege.
   ---  Repairing improvements now modifies the cost of the original construction based 
        upon the extent of the damage.  This was an oversight in v0.03.
   ---  New Improvement: Improved Roads (any) improves weekly income and doubles the 
        normal daily recovery rate of prosperity and progress towards recovering from 
        being looted.
   ---  New Improvement: Fire Brigade (any) reduces the chance of improvements being 
        damaged during a raid by 33%.  Cannot be damaged itself.
   ---  New Improvement: Forge (villages) improves a village elder’s available cash and 
        adds weapons to his sellable merchandise.
   ---  New Improvement: Mercenary Chapterhouse (towns) increases the number of mercenaries 
        available in the tavern by 8 and reduces the cost of hiring them by 15%.
   ---  New Improvement: Escape Tunnels (castles, towns) provides a 90% chance that you or 
        a lord will escape from a town under siege when defending it.  If damaged these 
        tunnels become less reliable.
   ---  New Improvement: Guild of Merchants (towns) increases town tariffs by 8% and raises 
        ideal prosperity by 3%.  (Requires: Improved Roads & Marketplace)

* Companion Role Updates:
   ---  The Storekeeper will now actually get rid of rotted food versus simply say he is 
        doing so.

* Included: "Troop Ratio Bar" 1.0 by rubik.

* When you are attacked in the tavern you’ll no longer be forced to unequip your ranged 
  weapons and the tavern keeper will only warn you once not to shoot ranged weapons.

* You and the AI are now always captured if defending a castle from siege and lose.


##############################################################################################
                                           Version 0.03
                                         Released 6/22/12
##############################################################################################
* Added new dialog options for noble prisoners held captive.
   ---	You can attempt to persuade a captive king to make peace, but you must be a king or 
        the marshal of a faction to do this.  (persuasion based)
   ---	You can attempt to intimidate a captive king into relinquishing his claim to the 
        throne causing his kingdom to follow your banner.  This is exceptionally difficult to 
        do unless your empire easily out powers theirs.  You must be a king to attempt this.
   ---	You can attempt to ransom a noble for 60%.  With a high enough persuasion you can 
        increase this to 120%, but there is some penalties involved and it is a gamble on if 
        it works.  (persuasion based)

* Removed the thrusting attack from the two-handed Iron Mace.  It looked silly.

* Disabling companion complaints also prevents a companion from leaving on their own.

* Skill Changes (testing these out):
   ---	Power Draw now functions based upon the Agility attribute.
   ---	Shield now functions based upon the Strength attribute.
   ---	Persuasion now functions based upon the Charisma attribute.

* Party Size Changes:
   ---	Players now receive same party size boosts the AI receive for fiefs, being marshal 
        or being king.
   ---	Charisma's contribution to party size improved from 1 to 2/point.
   ---	Leadership's contribution to party size improved from 5 to 8/point.

* You now automatically gain relation boosts with allied heroes that fight in the same 
        battle as you.  Kings and marshals receive a small boost to this while enemies may 
        ignore it.

* Fixed a dialog bug displaying incorrect text when granting a fief to a vassal.

* Center Improvements:
   ---	Villages, castles & towns may now have three improvements building in parallel.
   ---	Improvement construction time has been reduced by 33%.
   ---	You can now cancel work on improvements mid-construction.  All progress is lost.
   ---	Improvements can now be damaged by raiding.  Once damaged they must be repaired to 
        get full benefit again.  If allowed to deteriorate too far they will be destroyed.
   ---	You will lose 2 relation with the town for each building destroyed.
   ---	New Improvement: Local garrison (village) doubles the amount of time needed to raid 
        a village and prevents bandits from infesting it.  Costs a weekly upkeep.
   ---	New Improvement: Planting Grain (village, castle) costs 3 bags of grain and takes 
        60 days to complete (unmodified by engineering), but returns 5,000 denars one time 
        profit.
   ---	New Improvement: Armoury (castle, town) allows replenishment of a siege defenders' 
        ranged ammunition during combat.  Costs a weekly upkeep.
   ---	New Improvement: Marketplace (any) improves prosperity by 3% and income by 5% in 
        town.

* Companion Role Updates:
   ---	The Gaoler will no longer attempt to sell 0 prisoners upon entering town when only 
        hero prisoners exist in the party.
   ---	The Gaoler will now transfer any prisoners available (including heroes) to a prison 
        of a castle that you own upon entry.



##############################################################################################
                                           Version 0.02
                                         Released 6/18/12
##############################################################################################
* Fixed a dialog issue when asking a village elder for quests while not a noble.

* Companion relation report & assign party roles are now disabled menus if you have no 
        companions.

* Fixed a bug with script_auto_buy_food to prevent it misfiring upon leaving a castle.

* Refined slaughtering of cattle to allow storekeeper companion to loot the beef.

* When companions win prizes from a tournament they automatically give them to the 
        player.

* Added a "gaoler" companion role for the companion management system.
   ---	Uses his prisoner management skill instead of yours for determining prisoner limit.
   ---	Will automatically sell any non-quest related prisoners upon entering a town with a 
        ransom broker present.  Companion receives 15% of the take as payment.

* Added a "quartermaster" companion role for the companion management system.
   ---	Collects all valuable battlefield loot from the auto-loot screen.
   ---	Sells any goods or gear stored upon entering town and receives 15% of the earnings.

* Imposed maximum relation gains/losses for nobles at a tournament during a feast.

* Removed courtship benefit to relation gain on winning a tournament if you are married.

* Limited town relation gain to maximum of 3 upon winning a tournament.

* Experience gained due to high intelligence is capped at 50xp per kill during 
        tournaments.


##############################################################################################
                                           Version 0.01
                                         Released 6/8/12
##############################################################################################
* Mercenary Contracts
   ---	Increased payment for mercenary contracts to scale with player party upkeep, player 
        persuasion, and player + companion levels.
   ---	Failure to report to the marshal, scout as requested or join in sieges as ordered will 
        cause the contract to immediately end.

* Added ability to join either side in a battle as well as information on your 
        relationship with each side.

* Included: "Dynamic Troop Tree Viewer" by Dunde.

* Included: "Killer Regeneration" by Windyplains.

* Included: "XGM Mod Options" by Sphere with updates by Caba'drin.

* Included: "Tournament Play Enhancements" 1.5.2 by Windyplains.
   ---	Includes "Arena Overhaul Mod" by Adorno.

* Included: "Companion Management System" (beta) by Windyplains.

* Included: "Character Creation Panel" 1.0.7 by Windyplains.

* Added cheat to disable companion complaints.

* Lords who are holding a feast will still gain +1 relation with you for attending even 
        if you have 10+ relation with them already.

* Altered native quest "raise_troops" to allow turning in a partial number of the 
        requested troops for a small duration increase.

* Included: "Pre-Battle Orders & Deployment" 0.96.3 by Caba'drin
   ---	Allows pre-deployment options & phase prior to beginning combat.
   ---	Adds special command for "volley fire".
   ---	Adds special command for "spear bracing".
   ---	Adds special command for "skirmish mode".
   ---	Adds player option to disable companion complaints.
   ---	Adds player option to enable battle continuation.
   ---	Includes post-death "battle camera" by MadVader.

* Included: "Battle Formations" by Motomataru.

* Included: "Quest Utilities" by Windyplains.

* Included: "Quest Pack 3" (1.0) by Windyplains.
   ---	Adds Quest: Summoned to Hall
   ---	Adds Quest: Patrol for Bandits
   ---	Adds Quest: Mercenaries for Hire
   ---	Adds Quest: Root Them Out
   ---	Adds Quest: Escort Prisoners to Salt Mines

* Added "prisoner caravans" that appear to move large prisoner populations from castles 
        to the salt mines and return back with their sale value.  These caravans are raidable.

* Added option to speak with village elder to the village menu. (Custom Commander)

* Added game option to block popup menu notifications for factions going to war, making 
        peace, calling a truce or being involved in a border incident if you do not belong to 
        either faction.

* Heroes earn additional experienced based on intelligence above 10 when in combat.

* Added a quest menu for village elder quests.
