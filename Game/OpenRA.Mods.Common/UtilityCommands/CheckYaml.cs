#region Copyright & License Information
/*
 * Copyright 2007-2016 The OpenRA Developers (see AUTHORS)
 * This file is part of OpenRA, which is free software. It is made
 * available to you under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version. For more
 * information, see COPYING.
 */
#endregion

using System;
using System.Collections.Generic;
using System.Linq;
using OpenRA.Traits;

namespace OpenRA.Mods.Common.UtilityCommands
{
	class CheckYaml : IUtilityCommand
	{
		public string Name { get { return "--check-yaml"; } }

		static int errors = 0;

		// mimic Windows compiler error format
		static void EmitError(string e)
		{
			Console.WriteLine("OpenRA.Utility(1,1): Error: {0}", e);
			++errors;
		}

		static void EmitWarning(string e)
		{
			Console.WriteLine("OpenRA.Utility(1,1): Warning: {0}", e);
		}

		public bool ValidateArguments(string[] args)
		{
			return true;
		}

		[Desc("[MAPFILE]", "Check a mod or map for certain yaml errors.")]
		public void Run(ModData modData, string[] args)
		{
			// HACK: The engine code assumes that Game.modData is set.
			Game.ModData = modData;

			try
			{
				Log.AddChannel("debug", null);
				Log.AddChannel("perf", null);

				// bind some nonfatal error handling into FieldLoader, so we don't just *explode*.
				ObjectCreator.MissingTypeAction = s => EmitError("Missing Type: {0}".F(s));
				FieldLoader.UnknownFieldAction = (s, f) => EmitError("FieldLoader: Missing field `{0}` on `{1}`".F(s, f.Name));

				var maps = new List<Map>();
				if (args.Length < 2)
				{
					Console.WriteLine("Testing mod: {0}".F(modData.Manifest.Mod.Title));

					// Run all rule checks on the default mod rules.
					CheckRules(modData, modData.DefaultRules);

					// Run all generic (not mod-level) checks here.
					foreach (var customPassType in modData.ObjectCreator.GetTypesImplementing<ILintPass>())
					{
						try
						{
							var customPass = (ILintPass)modData.ObjectCreator.CreateBasic(customPassType);
							customPass.Run(EmitError, EmitWarning, modData);
						}
						catch (Exception e)
						{
							EmitError("{0} failed with exception: {1}".F(customPassType, e));
						}
					}

					modData.MapCache.LoadMaps();
					maps.AddRange(modData.MapCache
						.Where(m => m.Status == MapStatus.Available)
						.Select(m => new Map(modData, m.Package)));
				}
				else
					maps.Add(new Map(modData, modData.ModFiles.OpenPackage(args[1])));

				foreach (var testMap in maps)
				{
					Console.WriteLine("Testing map: {0}".F(testMap.Title));

					// Run all rule checks on the map if it defines custom rules.
					if (testMap.RuleDefinitions != null || testMap.VoiceDefinitions != null || testMap.WeaponDefinitions != null)
						CheckRules(modData, testMap.Rules, testMap);

					// Run all map-level checks here.
					foreach (var customMapPassType in modData.ObjectCreator.GetTypesImplementing<ILintMapPass>())
					{
						try
						{
							var customMapPass = (ILintMapPass)modData.ObjectCreator.CreateBasic(customMapPassType);
							customMapPass.Run(EmitError, EmitWarning, testMap);
						}
						catch (Exception e)
						{
							EmitError("{0} failed with exception: {1}".F(customMapPassType, e));
						}
					}
				}

				if (errors > 0)
				{
					Console.WriteLine("Errors: {0}", errors);
					Environment.Exit(1);
				}
			}
			catch (Exception e)
			{
				EmitError("Failed with exception: {0}".F(e));
				Environment.Exit(1);
			}
		}

		void CheckRules(ModData modData, Ruleset rules, Map map = null)
		{
			foreach (var customRulesPassType in modData.ObjectCreator.GetTypesImplementing<ILintRulesPass>())
			{
				try
				{
					var customRulesPass = (ILintRulesPass)modData.ObjectCreator.CreateBasic(customRulesPassType);
					customRulesPass.Run(EmitError, EmitWarning, rules);
				}
				catch (Exception e)
				{
					EmitError("{0} failed with exception: {1}".F(customRulesPassType, e));
				}
			}
		}
	}
}