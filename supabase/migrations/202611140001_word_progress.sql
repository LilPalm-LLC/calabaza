-- Per-user review state only. Vocabulary and typed answers are not stored.
create table if not exists public.word_progress (
    user_id uuid not null references auth.users (id) on delete cascade,
    word_id text not null check (length(word_id) between 1 and 100),
    status text not null check (status in ('learning', 'known')),
    last_reviewed_at timestamptz not null default now(),
    primary key (user_id, word_id)
);

alter table public.word_progress enable row level security;
alter table public.word_progress force row level security;

revoke all on table public.word_progress from anon, authenticated;
grant select, insert, update, delete on table public.word_progress to authenticated;

drop policy if exists "Users read their own word progress" on public.word_progress;
create policy "Users read their own word progress"
    on public.word_progress for select to authenticated
    using ((select auth.uid()) = user_id);

drop policy if exists "Users add their own word progress" on public.word_progress;
create policy "Users add their own word progress"
    on public.word_progress for insert to authenticated
    with check ((select auth.uid()) = user_id);

drop policy if exists "Users update their own word progress" on public.word_progress;
create policy "Users update their own word progress"
    on public.word_progress for update to authenticated
    using ((select auth.uid()) = user_id)
    with check ((select auth.uid()) = user_id);

drop policy if exists "Users delete their own word progress" on public.word_progress;
create policy "Users delete their own word progress"
    on public.word_progress for delete to authenticated
    using ((select auth.uid()) = user_id);
