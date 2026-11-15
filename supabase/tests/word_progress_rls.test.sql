begin;

create extension if not exists pgtap with schema extensions;
select plan(12);

-- Isolated synthetic fixtures. No personal learner data is used.
insert into auth.users (id, aud, role, email, encrypted_password, email_confirmed_at, created_at, updated_at)
values
 ('11111111-1111-4111-8111-111111111111','authenticated','authenticated','calabaza-a@example.test','',now(),now(),now()),
 ('22222222-2222-4222-8222-222222222222','authenticated','authenticated','calabaza-b@example.test','',now(),now(),now());

insert into public.word_progress (user_id, word_id, status, last_reviewed_at)
values
 ('11111111-1111-4111-8111-111111111111','fixture-own','learning',now()),
 ('22222222-2222-4222-8222-222222222222','fixture-private','known',now());

set local role authenticated;
select set_config('request.jwt.claim.sub','11111111-1111-4111-8111-111111111111',true);
select set_config('request.jwt.claim.role','authenticated',true);
select set_config('request.jwt.claims','{"sub":"11111111-1111-4111-8111-111111111111","role":"authenticated","aud":"authenticated"}',true);

select is((select count(*)::int from public.word_progress where word_id='fixture-own'),1,'user A can read own progress');
select is((select count(*)::int from public.word_progress where word_id='fixture-private'),0,'user A cannot read user B progress');
select lives_ok($$insert into public.word_progress(user_id,word_id,status) values ('11111111-1111-4111-8111-111111111111','fixture-added','known')$$,'user A can add own progress');
select throws_ok($$insert into public.word_progress(user_id,word_id,status) values ('22222222-2222-4222-8222-222222222222','fixture-forged','known')$$,'42501',null,'user A cannot add progress for user B');
select lives_ok($$update public.word_progress set status='learning' where word_id='fixture-private'$$,'user A cannot update user B rows');
select lives_ok($$delete from public.word_progress where word_id='fixture-private'$$,'user A cannot delete user B rows');

reset role;
set local role authenticated;
select set_config('request.jwt.claim.sub','22222222-2222-4222-8222-222222222222',true);
select set_config('request.jwt.claim.role','authenticated',true);
select set_config('request.jwt.claims','{"sub":"22222222-2222-4222-8222-222222222222","role":"authenticated","aud":"authenticated"}',true);

select is((select count(*)::int from public.word_progress where word_id='fixture-private'),1,'user B can read own progress');
select is((select count(*)::int from public.word_progress where word_id='fixture-own'),0,'user B cannot read user A progress');

reset role;
set local role anon;
select set_config('request.jwt.claim.role','anon',true);
select set_config('request.jwt.claims','{"role":"anon","aud":"anon"}',true);
select throws_ok($$select word_id from public.word_progress$$,'42501',null,'unauthenticated user cannot read progress');
select throws_ok($$insert into public.word_progress(user_id,word_id,status) values ('11111111-1111-4111-8111-111111111111','fixture-anon','known')$$,'42501',null,'unauthenticated user cannot write progress');

reset role;
select is((select status from public.word_progress where word_id='fixture-private'),'known','user B row remains unchanged');
select is((select count(*)::int from public.word_progress where word_id='fixture-added'),1,'user A row was saved');
select * from finish();
rollback;
