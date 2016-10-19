#region Copyright & License Information
/*
* Copyright 2007-2015 The OpenRA Developers (see AUTHORS)
* This file is part of OpenRA, which is free software. It is made
* available to you under the terms of the GNU General Public License
* as published by the Free Software Foundation. For more information,
* see COPYING.
*/
#endregion

using System;
using System.Linq;
using OpenRA.Mods.Common.Traits;
using OpenRA.Traits;

namespace OpenRA.Mods.D2k.Traits
{
	class SandwormInfo : WandersInfo, Requires<MobileInfo>, Requires<AttackBaseInfo>
	{
		[Desc("Time between rescanning for targets (in ticks).")]
		public readonly int TargetRescanInterval = 125;

		[Desc("The radius in which the worm \"searches\" for targets.")]
		public readonly WDist MaxSearchRadius = WDist.FromCells(20);

		[Desc("The range at which the worm launches an attack regardless of noise levels.")]
		public readonly WDist IgnoreNoiseAttackRange = WDist.FromCells(3);

		[Desc("The chance this actor has of disappearing after it attacks (in %).")]
		public readonly int ChanceToDisappear = 100;

		public override object Create(ActorInitializer init) { return new Sandworm(init.Self, this); }
	}

	class Sandworm : Wanders, ITick, INotifyActorDisposing
	{
		public readonly SandwormInfo Info;

		readonly WormManager manager;
		readonly Mobile mobile;
		readonly AttackBase attackTrait;

		public bool IsMovingTowardTarget { get; private set; }

		public bool IsAttacking;

		int targetCountdown;

		public Sandworm(Actor self, SandwormInfo info)
			: base(self, info)
		{
			Info = info;
			mobile = self.Trait<Mobile>();
			attackTrait = self.Trait<AttackBase>();
			manager = self.World.WorldActor.Trait<WormManager>();
		}

		public override void DoAction(Actor self, CPos targetCell)
		{
			IsMovingTowardTarget = false;

			RescanForTargets(self);

			if (IsMovingTowardTarget)
				return;

			self.QueueActivity(mobile.MoveWithinRange(Target.FromCell(self.World, targetCell, SubCell.Any), WDist.FromCells(1)));
		}

		public void Tick(Actor self)
		{
			if (--targetCountdown > 0 || IsAttacking || !self.IsInWorld)
				return;

			RescanForTargets(self);
		}

		void RescanForTargets(Actor self)
		{
			targetCountdown = Info.TargetRescanInterval;

			// If close enough, we don't care about other actors.
			var target = self.World.FindActorsInCircle(self.CenterPosition, Info.IgnoreNoiseAttackRange)
				.FirstOrDefault(x => attackTrait.HasAnyValidWeapons(Target.FromActor(x)));
			if (target != null)
			{
				self.CancelActivity();
				attackTrait.ResolveOrder(self, new Order("Attack", target, true) { TargetActor = target });
				return;
			}

			Func<Actor, bool> isValidTarget = a =>
			{
				if (!a.Info.HasTraitInfo<AttractsWormsInfo>())
					return false;

				return mobile.CanEnterCell(a.Location, null, false);
			};

			var actorsInRange = self.World.FindActorsInCircle(self.CenterPosition, Info.MaxSearchRadius)
				.Where(isValidTarget).SelectMany(a => a.TraitsImplementing<AttractsWorms>());

			var noiseDirection = actorsInRange.Aggregate(WVec.Zero, (a, b) => a + b.AttractionAtPosition(self.CenterPosition));

			// No target was found
			if (noiseDirection == WVec.Zero)
				return;

			var moveTo = self.World.Map.CellContaining(self.CenterPosition + noiseDirection);

			while (!self.World.Map.Contains(moveTo) || !mobile.CanEnterCell(moveTo, null, false))
			{
				noiseDirection /= 2;
				moveTo = self.World.Map.CellContaining(self.CenterPosition + noiseDirection);
			}

			// Don't get stuck when the noise is distributed evenly! This will make the worm wander instead of trying to move to where it already is
			if (moveTo == self.Location)
			{
				self.CancelActivity();
				return;
			}

			self.QueueActivity(false, mobile.MoveTo(moveTo, 3));
			IsMovingTowardTarget = true;
		}

		bool disposed;
		public void Disposing(Actor self)
		{
			if (disposed)
				return;

			manager.DecreaseWormCount();
			disposed = true;
		}
	}
}