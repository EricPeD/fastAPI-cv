2025-11-28 23:13:43,285 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:43,286 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:43,402 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:43,495 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:43,496 - src.config - INFO - Petición 4e2d804c-9455-43a6-915f-0d855141aaa4 registrada en la base de datos.
2025-11-28 23:13:43,496 - src.config - INFO - Archivo 'sample_cv_variant_01.pdf' guardado temporalmente como '34f104ad-3fee-4a3d-9dcf-d176670d1585_sample_cv_variant_01.pdf' para la petición 4e2d804c-9455-43a6-915f-0d855141aaa4.
2025-11-28 23:13:43,496 - src.config - INFO - Tarea de procesamiento para la petición 4e2d804c-9455-43a6-915f-0d855141aaa4 añadida a BackgroundTasks.
INFO:     127.0.0.1:43072 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:43,496 - src.config - INFO - Iniciando procesamiento de CV para la petición: 4e2d804c-9455-43a6-915f-0d855141aaa4
2025-11-28 23:13:43,586 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.4e2d804c-9455-43a6-915f-0d855141aaa4 "HTTP/2 200 OK"
2025-11-28 23:13:43,587 - src.config - INFO - Petición 4e2d804c-9455-43a6-915f-0d855141aaa4 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:43,589 - src.config - INFO - Procesando archivo 34f104ad-3fee-4a3d-9dcf-d176670d1585_sample_cv_variant_01.pdf con tipo MIME: application/pdf
2025-11-28 23:13:43,595 - src.config - INFO - Texto extraído del CV para la petición 4e2d804c-9455-43a6-915f-0d855141aaa4. Longitud: 2096
2025-11-28 23:13:43,849 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:43,849 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:43,941 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:44,025 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:44,026 - src.config - INFO - Petición 2e78a3be-6c26-4e93-9e98-e724d0714c34 registrada en la base de datos.
2025-11-28 23:13:44,026 - src.config - INFO - Archivo 'sample_cv_variant_02.pdf' guardado temporalmente como '205abb17-96c6-4921-a428-a42579e2faa2_sample_cv_variant_02.pdf' para la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34.
2025-11-28 23:13:44,026 - src.config - INFO - Tarea de procesamiento para la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34 añadida a BackgroundTasks.
INFO:     127.0.0.1:43076 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:44,026 - src.config - INFO - Iniciando procesamiento de CV para la petición: 2e78a3be-6c26-4e93-9e98-e724d0714c34
2025-11-28 23:13:44,099 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.2e78a3be-6c26-4e93-9e98-e724d0714c34 "HTTP/2 200 OK"
2025-11-28 23:13:44,099 - src.config - INFO - Petición 2e78a3be-6c26-4e93-9e98-e724d0714c34 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:44,100 - src.config - INFO - Procesando archivo 205abb17-96c6-4921-a428-a42579e2faa2_sample_cv_variant_02.pdf con tipo MIME: application/pdf
2025-11-28 23:13:44,102 - src.config - INFO - Texto extraído del CV para la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34. Longitud: 2096
2025-11-28 23:13:44,190 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:44,190 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:44,275 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:44,369 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:44,369 - src.config - INFO - Petición d33650f7-e7d9-4872-90ec-67ae55b30355 registrada en la base de datos.
2025-11-28 23:13:44,370 - src.config - INFO - Archivo 'sample_cv_variant_03.pdf' guardado temporalmente como '48e88e74-e04f-43de-b2bb-12612c7c5fb3_sample_cv_variant_03.pdf' para la petición d33650f7-e7d9-4872-90ec-67ae55b30355.
2025-11-28 23:13:44,370 - src.config - INFO - Tarea de procesamiento para la petición d33650f7-e7d9-4872-90ec-67ae55b30355 añadida a BackgroundTasks.
INFO:     127.0.0.1:43080 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:44,370 - src.config - INFO - Iniciando procesamiento de CV para la petición: d33650f7-e7d9-4872-90ec-67ae55b30355
2025-11-28 23:13:44,453 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.d33650f7-e7d9-4872-90ec-67ae55b30355 "HTTP/2 200 OK"
2025-11-28 23:13:44,453 - src.config - INFO - Petición d33650f7-e7d9-4872-90ec-67ae55b30355 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:44,453 - src.config - INFO - Procesando archivo 48e88e74-e04f-43de-b2bb-12612c7c5fb3_sample_cv_variant_03.pdf con tipo MIME: application/pdf
2025-11-28 23:13:44,455 - src.config - INFO - Texto extraído del CV para la petición d33650f7-e7d9-4872-90ec-67ae55b30355. Longitud: 2096
2025-11-28 23:13:44,566 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:44,567 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:44,649 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:44,728 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:44,728 - src.config - INFO - Petición 12992dcf-7eaf-42b6-b4ed-728882e04427 registrada en la base de datos.
2025-11-28 23:13:44,728 - src.config - INFO - Archivo 'sample_cv_variant_04.pdf' guardado temporalmente como '0fe3ce02-f389-4caf-bebe-fec24bc24d41_sample_cv_variant_04.pdf' para la petición 12992dcf-7eaf-42b6-b4ed-728882e04427.
2025-11-28 23:13:44,728 - src.config - INFO - Tarea de procesamiento para la petición 12992dcf-7eaf-42b6-b4ed-728882e04427 añadida a BackgroundTasks.
INFO:     127.0.0.1:43094 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:44,729 - src.config - INFO - Iniciando procesamiento de CV para la petición: 12992dcf-7eaf-42b6-b4ed-728882e04427
2025-11-28 23:13:44,805 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.12992dcf-7eaf-42b6-b4ed-728882e04427 "HTTP/2 200 OK"
2025-11-28 23:13:44,805 - src.config - INFO - Petición 12992dcf-7eaf-42b6-b4ed-728882e04427 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:44,805 - src.config - INFO - Procesando archivo 0fe3ce02-f389-4caf-bebe-fec24bc24d41_sample_cv_variant_04.pdf con tipo MIME: application/pdf
2025-11-28 23:13:44,807 - src.config - INFO - Texto extraído del CV para la petición 12992dcf-7eaf-42b6-b4ed-728882e04427. Longitud: 2096
2025-11-28 23:13:44,870 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:44,870 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:44,939 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:45,023 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:45,024 - src.config - INFO - Petición 4129bfe2-6bc8-45b5-91db-8991be96e707 registrada en la base de datos.
2025-11-28 23:13:45,024 - src.config - INFO - Archivo 'sample_cv_variant_05.pdf' guardado temporalmente como '538256c8-391c-4fec-8a9e-59898a112edc_sample_cv_variant_05.pdf' para la petición 4129bfe2-6bc8-45b5-91db-8991be96e707.
2025-11-28 23:13:45,024 - src.config - INFO - Tarea de procesamiento para la petición 4129bfe2-6bc8-45b5-91db-8991be96e707 añadida a BackgroundTasks.
INFO:     127.0.0.1:43102 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:45,024 - src.config - INFO - Iniciando procesamiento de CV para la petición: 4129bfe2-6bc8-45b5-91db-8991be96e707
2025-11-28 23:13:45,102 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.4129bfe2-6bc8-45b5-91db-8991be96e707 "HTTP/2 200 OK"
2025-11-28 23:13:45,102 - src.config - INFO - Petición 4129bfe2-6bc8-45b5-91db-8991be96e707 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:45,102 - src.config - INFO - Procesando archivo 538256c8-391c-4fec-8a9e-59898a112edc_sample_cv_variant_05.pdf con tipo MIME: application/pdf
2025-11-28 23:13:45,104 - src.config - INFO - Texto extraído del CV para la petición 4129bfe2-6bc8-45b5-91db-8991be96e707. Longitud: 2096
2025-11-28 23:13:45,184 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:45,185 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:45,265 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:45,331 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:45,331 - src.config - INFO - Petición 2370cfd6-ff7d-4302-a3df-b0a712f44408 registrada en la base de datos.
2025-11-28 23:13:45,332 - src.config - INFO - Archivo 'sample_cv_variant_06.pdf' guardado temporalmente como '058ffc95-eca0-4f12-a671-35fe66101442_sample_cv_variant_06.pdf' para la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408.
2025-11-28 23:13:45,332 - src.config - INFO - Tarea de procesamiento para la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408 añadida a BackgroundTasks.
INFO:     127.0.0.1:43104 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:45,332 - src.config - INFO - Iniciando procesamiento de CV para la petición: 2370cfd6-ff7d-4302-a3df-b0a712f44408
2025-11-28 23:13:45,398 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.2370cfd6-ff7d-4302-a3df-b0a712f44408 "HTTP/2 200 OK"
2025-11-28 23:13:45,399 - src.config - INFO - Petición 2370cfd6-ff7d-4302-a3df-b0a712f44408 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:45,399 - src.config - INFO - Procesando archivo 058ffc95-eca0-4f12-a671-35fe66101442_sample_cv_variant_06.pdf con tipo MIME: application/pdf
2025-11-28 23:13:45,401 - src.config - INFO - Texto extraído del CV para la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408. Longitud: 2096
2025-11-28 23:13:45,470 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:45,470 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:45,535 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:45,612 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:45,612 - src.config - INFO - Petición b242e543-e986-465b-b15d-3a2bee700826 registrada en la base de datos.
2025-11-28 23:13:45,613 - src.config - INFO - Archivo 'sample_cv_variant_07.pdf' guardado temporalmente como '3bd32bb9-e2e9-4182-9109-a0fdeda0278f_sample_cv_variant_07.pdf' para la petición b242e543-e986-465b-b15d-3a2bee700826.
2025-11-28 23:13:45,613 - src.config - INFO - Tarea de procesamiento para la petición b242e543-e986-465b-b15d-3a2bee700826 añadida a BackgroundTasks.
INFO:     127.0.0.1:43110 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:45,613 - src.config - INFO - Iniciando procesamiento de CV para la petición: b242e543-e986-465b-b15d-3a2bee700826
2025-11-28 23:13:45,678 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.b242e543-e986-465b-b15d-3a2bee700826 "HTTP/2 200 OK"
2025-11-28 23:13:45,678 - src.config - INFO - Petición b242e543-e986-465b-b15d-3a2bee700826 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:45,679 - src.config - INFO - Procesando archivo 3bd32bb9-e2e9-4182-9109-a0fdeda0278f_sample_cv_variant_07.pdf con tipo MIME: application/pdf
2025-11-28 23:13:45,680 - src.config - INFO - Texto extraído del CV para la petición b242e543-e986-465b-b15d-3a2bee700826. Longitud: 2096
2025-11-28 23:13:45,747 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:45,747 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:45,813 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:45,889 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:45,896 - src.config - INFO - Petición 1757e7f0-a809-443a-82df-c24a999cdc64 registrada en la base de datos.
2025-11-28 23:13:45,897 - src.config - INFO - Archivo 'sample_cv_variant_08.pdf' guardado temporalmente como 'e945e203-4d79-4f7e-b82b-3ac66ccaad7e_sample_cv_variant_08.pdf' para la petición 1757e7f0-a809-443a-82df-c24a999cdc64.
2025-11-28 23:13:45,897 - src.config - INFO - Tarea de procesamiento para la petición 1757e7f0-a809-443a-82df-c24a999cdc64 añadida a BackgroundTasks.
INFO:     127.0.0.1:43124 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:45,897 - src.config - INFO - Iniciando procesamiento de CV para la petición: 1757e7f0-a809-443a-82df-c24a999cdc64
2025-11-28 23:13:45,967 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.1757e7f0-a809-443a-82df-c24a999cdc64 "HTTP/2 200 OK"
2025-11-28 23:13:45,967 - src.config - INFO - Petición 1757e7f0-a809-443a-82df-c24a999cdc64 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:45,968 - src.config - INFO - Procesando archivo e945e203-4d79-4f7e-b82b-3ac66ccaad7e_sample_cv_variant_08.pdf con tipo MIME: application/pdf
2025-11-28 23:13:45,969 - src.config - INFO - Texto extraído del CV para la petición 1757e7f0-a809-443a-82df-c24a999cdc64. Longitud: 2096
2025-11-28 23:13:46,125 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:46,125 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:46,193 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:46,272 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:46,275 - src.config - INFO - Petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6 registrada en la base de datos.
2025-11-28 23:13:46,278 - src.config - INFO - Archivo 'sample_cv_variant_09.pdf' guardado temporalmente como '0314c15b-f0c2-4bec-97a7-10652f1fea76_sample_cv_variant_09.pdf' para la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6.
2025-11-28 23:13:46,278 - src.config - INFO - Tarea de procesamiento para la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6 añadida a BackgroundTasks.
INFO:     127.0.0.1:43132 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:46,279 - src.config - INFO - Iniciando procesamiento de CV para la petición: e8c3ad95-f5e6-4733-9106-e8fa7467d6c6
2025-11-28 23:13:46,345 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.e8c3ad95-f5e6-4733-9106-e8fa7467d6c6 "HTTP/2 200 OK"
2025-11-28 23:13:46,345 - src.config - INFO - Petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:46,346 - src.config - INFO - Procesando archivo 0314c15b-f0c2-4bec-97a7-10652f1fea76_sample_cv_variant_09.pdf con tipo MIME: application/pdf
2025-11-28 23:13:46,347 - src.config - INFO - Texto extraído del CV para la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6. Longitud: 2096
2025-11-28 23:13:46,410 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:46,410 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:46,477 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:46,549 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:46,549 - src.config - INFO - Petición a5e0c829-0555-46a1-8b31-071eb282ff5d registrada en la base de datos.
2025-11-28 23:13:46,550 - src.config - INFO - Archivo 'sample_cv_variant_10.pdf' guardado temporalmente como '2c2dc546-464f-4e64-87bc-83c174c1f7ae_sample_cv_variant_10.pdf' para la petición a5e0c829-0555-46a1-8b31-071eb282ff5d.
2025-11-28 23:13:46,550 - src.config - INFO - Tarea de procesamiento para la petición a5e0c829-0555-46a1-8b31-071eb282ff5d añadida a BackgroundTasks.
INFO:     127.0.0.1:43136 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:46,550 - src.config - INFO - Iniciando procesamiento de CV para la petición: a5e0c829-0555-46a1-8b31-071eb282ff5d
2025-11-28 23:13:46,614 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.a5e0c829-0555-46a1-8b31-071eb282ff5d "HTTP/2 200 OK"
2025-11-28 23:13:46,615 - src.config - INFO - Petición a5e0c829-0555-46a1-8b31-071eb282ff5d y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:46,615 - src.config - INFO - Procesando archivo 2c2dc546-464f-4e64-87bc-83c174c1f7ae_sample_cv_variant_10.pdf con tipo MIME: application/pdf
2025-11-28 23:13:46,616 - src.config - INFO - Texto extraído del CV para la petición a5e0c829-0555-46a1-8b31-071eb282ff5d. Longitud: 2098
2025-11-28 23:13:46,683 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:46,683 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:46,750 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:46,827 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:46,827 - src.config - INFO - Petición c4be2761-9631-43f6-9509-ac894ae91dfa registrada en la base de datos.
2025-11-28 23:13:46,827 - src.config - INFO - Archivo 'sample_cv_variant_11.pdf' guardado temporalmente como 'cac717a2-f990-4764-b58c-fb8c3ccf331f_sample_cv_variant_11.pdf' para la petición c4be2761-9631-43f6-9509-ac894ae91dfa.
2025-11-28 23:13:46,828 - src.config - INFO - Tarea de procesamiento para la petición c4be2761-9631-43f6-9509-ac894ae91dfa añadida a BackgroundTasks.
INFO:     127.0.0.1:43152 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:46,828 - src.config - INFO - Iniciando procesamiento de CV para la petición: c4be2761-9631-43f6-9509-ac894ae91dfa
2025-11-28 23:13:46,893 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.c4be2761-9631-43f6-9509-ac894ae91dfa "HTTP/2 200 OK"
2025-11-28 23:13:46,893 - src.config - INFO - Petición c4be2761-9631-43f6-9509-ac894ae91dfa y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:46,893 - src.config - INFO - Procesando archivo cac717a2-f990-4764-b58c-fb8c3ccf331f_sample_cv_variant_11.pdf con tipo MIME: application/pdf
2025-11-28 23:13:46,895 - src.config - INFO - Texto extraído del CV para la petición c4be2761-9631-43f6-9509-ac894ae91dfa. Longitud: 2098
2025-11-28 23:13:46,965 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:46,965 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:47,034 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:47,098 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:47,099 - src.config - INFO - Petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789 registrada en la base de datos.
2025-11-28 23:13:47,099 - src.config - INFO - Archivo 'sample_cv_variant_12.pdf' guardado temporalmente como 'ca115bd8-c4e7-4f77-a0f4-c996d7acc671_sample_cv_variant_12.pdf' para la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789.
2025-11-28 23:13:47,099 - src.config - INFO - Tarea de procesamiento para la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789 añadida a BackgroundTasks.
INFO:     127.0.0.1:43162 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:47,099 - src.config - INFO - Iniciando procesamiento de CV para la petición: 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789
2025-11-28 23:13:47,163 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.8bd4fc82-594c-4a9b-a6f9-24fd4b95b789 "HTTP/2 200 OK"
2025-11-28 23:13:47,164 - src.config - INFO - Petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:47,164 - src.config - INFO - Procesando archivo ca115bd8-c4e7-4f77-a0f4-c996d7acc671_sample_cv_variant_12.pdf con tipo MIME: application/pdf
2025-11-28 23:13:47,165 - src.config - INFO - Texto extraído del CV para la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789. Longitud: 2098
2025-11-28 23:13:47,233 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:47,234 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:47,306 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:47,379 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:47,379 - src.config - INFO - Petición f7c7b097-8ba7-48a0-afc7-8208d891509d registrada en la base de datos.
2025-11-28 23:13:47,380 - src.config - INFO - Archivo 'sample_cv_variant_13.pdf' guardado temporalmente como 'f8fb0d0a-bedc-4f69-ba9e-47be1f763dc0_sample_cv_variant_13.pdf' para la petición f7c7b097-8ba7-48a0-afc7-8208d891509d.
2025-11-28 23:13:47,380 - src.config - INFO - Tarea de procesamiento para la petición f7c7b097-8ba7-48a0-afc7-8208d891509d añadida a BackgroundTasks.
INFO:     127.0.0.1:43178 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:47,380 - src.config - INFO - Iniciando procesamiento de CV para la petición: f7c7b097-8ba7-48a0-afc7-8208d891509d
2025-11-28 23:13:47,456 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.f7c7b097-8ba7-48a0-afc7-8208d891509d "HTTP/2 200 OK"
2025-11-28 23:13:47,457 - src.config - INFO - Petición f7c7b097-8ba7-48a0-afc7-8208d891509d y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:47,457 - src.config - INFO - Procesando archivo f8fb0d0a-bedc-4f69-ba9e-47be1f763dc0_sample_cv_variant_13.pdf con tipo MIME: application/pdf
2025-11-28 23:13:47,459 - src.config - INFO - Texto extraído del CV para la petición f7c7b097-8ba7-48a0-afc7-8208d891509d. Longitud: 2098
2025-11-28 23:13:47,541 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:47,541 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:47,691 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:47,754 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:47,754 - src.config - INFO - Petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114 registrada en la base de datos.
2025-11-28 23:13:47,755 - src.config - INFO - Archivo 'sample_cv_variant_14.pdf' guardado temporalmente como 'b050f3cc-ecde-480c-a9f4-debc10362ab7_sample_cv_variant_14.pdf' para la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114.
2025-11-28 23:13:47,755 - src.config - INFO - Tarea de procesamiento para la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114 añadida a BackgroundTasks.
INFO:     127.0.0.1:43188 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:47,755 - src.config - INFO - Iniciando procesamiento de CV para la petición: 4e3d5cc1-a858-4a10-97d7-fe61301f9114
2025-11-28 23:13:47,826 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.4e3d5cc1-a858-4a10-97d7-fe61301f9114 "HTTP/2 200 OK"
2025-11-28 23:13:47,826 - src.config - INFO - Petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:47,826 - src.config - INFO - Procesando archivo b050f3cc-ecde-480c-a9f4-debc10362ab7_sample_cv_variant_14.pdf con tipo MIME: application/pdf
2025-11-28 23:13:47,828 - src.config - INFO - Texto extraído del CV para la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114. Longitud: 2098
2025-11-28 23:13:47,897 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/api_keys?select=id_key%2Ckey_hash%2Cid_user&id_key=eq.082db487-cc96-4312-beed-ece21d33bc5d "HTTP/2 200 OK"
2025-11-28 23:13:47,899 - src.config - INFO - Solicitud de subida de CV recibida para el endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 por el usuario user_35u9sLsP8chFWAUEakiEKSFEjMg.
2025-11-28 23:13:47,962 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/endpoints?select=id_user%2Cinfo&id=eq.1edb42d6-2410-4e52-92a1-61ac958182a4 "HTTP/2 200 OK"
2025-11-28 23:13:48,025 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests "HTTP/2 201 Created"
2025-11-28 23:13:48,026 - src.config - INFO - Petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2 registrada en la base de datos.
2025-11-28 23:13:48,026 - src.config - INFO - Archivo 'sample_cv.pdf' guardado temporalmente como 'bce37ddf-dfd8-4343-8133-c72635763647_sample_cv.pdf' para la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2.
2025-11-28 23:13:48,026 - src.config - INFO - Tarea de procesamiento para la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2 añadida a BackgroundTasks.
INFO:     127.0.0.1:43062 - "POST /cv/1edb42d6-2410-4e52-92a1-61ac958182a4 HTTP/1.1" 202 Accepted
2025-11-28 23:13:48,026 - src.config - INFO - Iniciando procesamiento de CV para la petición: 73d664eb-2d31-4f24-a3a8-a6d66780f9d2
2025-11-28 23:13:48,098 - httpx - INFO - HTTP Request: GET https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?select=%2A%2Cendpoints%28info%29&id_request=eq.73d664eb-2d31-4f24-a3a8-a6d66780f9d2 "HTTP/2 200 OK"
2025-11-28 23:13:48,098 - src.config - INFO - Petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2 y endpoint 1edb42d6-2410-4e52-92a1-61ac958182a4 encontrados. Callback URL: https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559
2025-11-28 23:13:48,098 - src.config - INFO - Procesando archivo bce37ddf-dfd8-4343-8133-c72635763647_sample_cv.pdf con tipo MIME: application/pdf
2025-11-28 23:13:48,104 - src.config - INFO - Texto extraído del CV para la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2. Longitud: 2347
2025-11-28 23:13:57,269 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,275 - src.config - INFO - Información de CV extraída con éxito para la petición d33650f7-e7d9-4872-90ec-67ae55b30355.
2025-11-28 23:13:57,365 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.d33650f7-e7d9-4872-90ec-67ae55b30355 "HTTP/2 200 OK"
2025-11-28 23:13:57,365 - src.config - INFO - Estado de la petición d33650f7-e7d9-4872-90ec-67ae55b30355 actualizado a 'completed'.
2025-11-28 23:13:57,437 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:57,438 - src.config - INFO - Log insertado para la petición d33650f7-e7d9-4872-90ec-67ae55b30355.
2025-11-28 23:13:57,463 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,464 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,465 - src.config - INFO - Información de CV extraída con éxito para la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789.
2025-11-28 23:13:57,550 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.8bd4fc82-594c-4a9b-a6f9-24fd4b95b789 "HTTP/2 200 OK"
2025-11-28 23:13:57,550 - src.config - INFO - Estado de la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789 actualizado a 'completed'.
2025-11-28 23:13:57,617 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:57,618 - src.config - INFO - Log insertado para la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789.
2025-11-28 23:13:57,643 - src.config - INFO - Información de CV extraída con éxito para la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6.
2025-11-28 23:13:57,707 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.e8c3ad95-f5e6-4733-9106-e8fa7467d6c6 "HTTP/2 200 OK"
2025-11-28 23:13:57,708 - src.config - INFO - Estado de la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6 actualizado a 'completed'.
2025-11-28 23:13:57,773 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:57,774 - src.config - INFO - Log insertado para la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6.
2025-11-28 23:13:57,799 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,800 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,800 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,801 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:57,802 - src.config - INFO - Información de CV extraída con éxito para la petición f7c7b097-8ba7-48a0-afc7-8208d891509d.
2025-11-28 23:13:57,867 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.f7c7b097-8ba7-48a0-afc7-8208d891509d "HTTP/2 200 OK"
2025-11-28 23:13:57,867 - src.config - INFO - Estado de la petición f7c7b097-8ba7-48a0-afc7-8208d891509d actualizado a 'completed'.
2025-11-28 23:13:57,955 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:57,956 - src.config - INFO - Log insertado para la petición f7c7b097-8ba7-48a0-afc7-8208d891509d.
2025-11-28 23:13:57,981 - src.config - INFO - Información de CV extraída con éxito para la petición 4e2d804c-9455-43a6-915f-0d855141aaa4.
2025-11-28 23:13:58,050 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.4e2d804c-9455-43a6-915f-0d855141aaa4 "HTTP/2 200 OK"
2025-11-28 23:13:58,050 - src.config - INFO - Estado de la petición 4e2d804c-9455-43a6-915f-0d855141aaa4 actualizado a 'completed'.
2025-11-28 23:13:58,120 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:58,120 - src.config - INFO - Log insertado para la petición 4e2d804c-9455-43a6-915f-0d855141aaa4.
2025-11-28 23:13:58,145 - src.config - INFO - Información de CV extraída con éxito para la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114.
2025-11-28 23:13:58,211 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.4e3d5cc1-a858-4a10-97d7-fe61301f9114 "HTTP/2 200 OK"
2025-11-28 23:13:58,211 - src.config - INFO - Estado de la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114 actualizado a 'completed'.
2025-11-28 23:13:58,278 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:58,279 - src.config - INFO - Log insertado para la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114.
2025-11-28 23:13:58,303 - src.config - INFO - Información de CV extraída con éxito para la petición c4be2761-9631-43f6-9509-ac894ae91dfa.
2025-11-28 23:13:58,373 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.c4be2761-9631-43f6-9509-ac894ae91dfa "HTTP/2 200 OK"
2025-11-28 23:13:58,373 - src.config - INFO - Estado de la petición c4be2761-9631-43f6-9509-ac894ae91dfa actualizado a 'completed'.
2025-11-28 23:13:58,438 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:58,439 - src.config - INFO - Log insertado para la petición c4be2761-9631-43f6-9509-ac894ae91dfa.
2025-11-28 23:13:58,464 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:58,465 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:58,465 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:58,466 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:58,467 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:58,468 - src.config - INFO - Información de CV extraída con éxito para la petición 12992dcf-7eaf-42b6-b4ed-728882e04427.
2025-11-28 23:13:58,532 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.12992dcf-7eaf-42b6-b4ed-728882e04427 "HTTP/2 200 OK"
2025-11-28 23:13:58,533 - src.config - INFO - Estado de la petición 12992dcf-7eaf-42b6-b4ed-728882e04427 actualizado a 'completed'.
2025-11-28 23:13:58,597 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:58,597 - src.config - INFO - Log insertado para la petición 12992dcf-7eaf-42b6-b4ed-728882e04427.
2025-11-28 23:13:58,622 - src.config - INFO - Información de CV extraída con éxito para la petición a5e0c829-0555-46a1-8b31-071eb282ff5d.
2025-11-28 23:13:58,691 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.a5e0c829-0555-46a1-8b31-071eb282ff5d "HTTP/2 200 OK"
2025-11-28 23:13:58,691 - src.config - INFO - Estado de la petición a5e0c829-0555-46a1-8b31-071eb282ff5d actualizado a 'completed'.
2025-11-28 23:13:58,765 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:58,766 - src.config - INFO - Log insertado para la petición a5e0c829-0555-46a1-8b31-071eb282ff5d.
2025-11-28 23:13:58,790 - src.config - INFO - Información de CV extraída con éxito para la petición b242e543-e986-465b-b15d-3a2bee700826.
2025-11-28 23:13:58,854 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.b242e543-e986-465b-b15d-3a2bee700826 "HTTP/2 200 OK"
2025-11-28 23:13:58,854 - src.config - INFO - Estado de la petición b242e543-e986-465b-b15d-3a2bee700826 actualizado a 'completed'.
2025-11-28 23:13:58,919 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:58,919 - src.config - INFO - Log insertado para la petición b242e543-e986-465b-b15d-3a2bee700826.
2025-11-28 23:13:58,944 - src.config - INFO - Información de CV extraída con éxito para la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408.
2025-11-28 23:13:59,010 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.2370cfd6-ff7d-4302-a3df-b0a712f44408 "HTTP/2 200 OK"
2025-11-28 23:13:59,010 - src.config - INFO - Estado de la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408 actualizado a 'completed'.
2025-11-28 23:13:59,080 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:59,080 - src.config - INFO - Log insertado para la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408.
2025-11-28 23:13:59,106 - src.config - INFO - Información de CV extraída con éxito para la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34.
2025-11-28 23:13:59,174 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.2e78a3be-6c26-4e93-9e98-e724d0714c34 "HTTP/2 200 OK"
2025-11-28 23:13:59,174 - src.config - INFO - Estado de la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34 actualizado a 'completed'.
2025-11-28 23:13:59,241 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:59,242 - src.config - INFO - Log insertado para la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34.
2025-11-28 23:13:59,267 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:59,268 - src.config - INFO - Información de CV extraída con éxito para la petición 1757e7f0-a809-443a-82df-c24a999cdc64.
2025-11-28 23:13:59,333 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.1757e7f0-a809-443a-82df-c24a999cdc64 "HTTP/2 200 OK"
2025-11-28 23:13:59,333 - src.config - INFO - Estado de la petición 1757e7f0-a809-443a-82df-c24a999cdc64 actualizado a 'completed'.
2025-11-28 23:13:59,402 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:59,403 - src.config - INFO - Log insertado para la petición 1757e7f0-a809-443a-82df-c24a999cdc64.
2025-11-28 23:13:59,548 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,548 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 8bd4fc82-594c-4a9b-a6f9-24fd4b95b789.
2025-11-28 23:13:59,548 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,549 - src.config - INFO - Archivo temporal ca115bd8-c4e7-4f77-a0f4-c996d7acc671_sample_cv_variant_12.pdf eliminado.
2025-11-28 23:13:59,549 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición d33650f7-e7d9-4872-90ec-67ae55b30355.
2025-11-28 23:13:59,549 - src.config - INFO - Archivo temporal 48e88e74-e04f-43de-b2bb-12612c7c5fb3_sample_cv_variant_03.pdf eliminado.
2025-11-28 23:13:59,574 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,574 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición e8c3ad95-f5e6-4733-9106-e8fa7467d6c6.
2025-11-28 23:13:59,575 - src.config - INFO - Archivo temporal 0314c15b-f0c2-4bec-97a7-10652f1fea76_sample_cv_variant_09.pdf eliminado.
2025-11-28 23:13:59,578 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:13:59,580 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,580 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 4e2d804c-9455-43a6-915f-0d855141aaa4.
2025-11-28 23:13:59,580 - src.config - INFO - Archivo temporal 34f104ad-3fee-4a3d-9dcf-d176670d1585_sample_cv_variant_01.pdf eliminado.
2025-11-28 23:13:59,586 - src.config - INFO - Información de CV extraída con éxito para la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2.
2025-11-28 23:13:59,656 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.73d664eb-2d31-4f24-a3a8-a6d66780f9d2 "HTTP/2 200 OK"
2025-11-28 23:13:59,656 - src.config - INFO - Estado de la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2 actualizado a 'completed'.
2025-11-28 23:13:59,725 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:13:59,726 - src.config - INFO - Log insertado para la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2.
2025-11-28 23:13:59,751 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,751 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,751 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,752 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,752 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,752 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,753 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,753 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,753 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición b242e543-e986-465b-b15d-3a2bee700826.
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 2370cfd6-ff7d-4302-a3df-b0a712f44408.
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 2e78a3be-6c26-4e93-9e98-e724d0714c34.
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición a5e0c829-0555-46a1-8b31-071eb282ff5d.
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 1757e7f0-a809-443a-82df-c24a999cdc64.
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición f7c7b097-8ba7-48a0-afc7-8208d891509d.
2025-11-28 23:13:59,754 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición c4be2761-9631-43f6-9509-ac894ae91dfa.
2025-11-28 23:13:59,755 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 4e3d5cc1-a858-4a10-97d7-fe61301f9114.
2025-11-28 23:13:59,755 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 12992dcf-7eaf-42b6-b4ed-728882e04427.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal 3bd32bb9-e2e9-4182-9109-a0fdeda0278f_sample_cv_variant_07.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal 058ffc95-eca0-4f12-a671-35fe66101442_sample_cv_variant_06.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal 205abb17-96c6-4921-a428-a42579e2faa2_sample_cv_variant_02.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal 2c2dc546-464f-4e64-87bc-83c174c1f7ae_sample_cv_variant_10.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal e945e203-4d79-4f7e-b82b-3ac66ccaad7e_sample_cv_variant_08.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal f8fb0d0a-bedc-4f69-ba9e-47be1f763dc0_sample_cv_variant_13.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal cac717a2-f990-4764-b58c-fb8c3ccf331f_sample_cv_variant_11.pdf eliminado.
2025-11-28 23:13:59,755 - src.config - INFO - Archivo temporal b050f3cc-ecde-480c-a9f4-debc10362ab7_sample_cv_variant_14.pdf eliminado.
2025-11-28 23:13:59,756 - src.config - INFO - Archivo temporal 0fe3ce02-f389-4caf-bebe-fec24bc24d41_sample_cv_variant_04.pdf eliminado.
2025-11-28 23:13:59,909 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:13:59,909 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 73d664eb-2d31-4f24-a3a8-a6d66780f9d2.
2025-11-28 23:13:59,910 - src.config - INFO - Archivo temporal bce37ddf-dfd8-4343-8133-c72635763647_sample_cv.pdf eliminado.
2025-11-28 23:14:00,974 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-11-28 23:14:00,976 - src.config - INFO - Información de CV extraída con éxito para la petición 4129bfe2-6bc8-45b5-91db-8991be96e707.
2025-11-28 23:14:01,041 - httpx - INFO - HTTP Request: PATCH https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/requests?id_request=eq.4129bfe2-6bc8-45b5-91db-8991be96e707 "HTTP/2 200 OK"
2025-11-28 23:14:01,041 - src.config - INFO - Estado de la petición 4129bfe2-6bc8-45b5-91db-8991be96e707 actualizado a 'completed'.
2025-11-28 23:14:01,112 - httpx - INFO - HTTP Request: POST https://qmoqpylwjxkrutmepygl.supabase.co/rest/v1/request_logs "HTTP/2 201 Created"
2025-11-28 23:14:01,113 - src.config - INFO - Log insertado para la petición 4129bfe2-6bc8-45b5-91db-8991be96e707.
2025-11-28 23:14:01,361 - httpx - INFO - HTTP Request: POST https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 "HTTP/1.1 200 OK"
2025-11-28 23:14:01,362 - src.config - INFO - Resultado enviado al callback https://webhook.site/a5858e52-5c4f-465b-a338-ad6f9a15b559 para la petición 4129bfe2-6bc8-45b5-91db-8991be96e707.
2025-11-28 23:14:01,362 - src.config - INFO - Archivo temporal 538256c8-391c-4fec-8a9e-59898a112edc_sample_cv_variant_05.pdf eliminado.