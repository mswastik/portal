PGDMP                     
    x            app1db1    13.1    13.1 �    �           0    0    ENCODING    ENCODING     !   SET client_encoding = 'WIN1252';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16385    app1db1    DATABASE     f   CREATE DATABASE app1db1 WITH TEMPLATE = template0 ENCODING = 'WIN1252' LOCALE = 'English_India.1252';
    DROP DATABASE app1db1;
                admin    false            �            1259    16618    app1_bom    TABLE     �   CREATE TABLE public.app1_bom (
    id integer NOT NULL,
    qty numeric(9,4) NOT NULL,
    uom character varying(3) NOT NULL,
    active boolean NOT NULL,
    code_id integer
);
    DROP TABLE public.app1_bom;
       public         heap    admin    false            �            1259    16616    app1_bom_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_bom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.app1_bom_id_seq;
       public          admin    false    239            �           0    0    app1_bom_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.app1_bom_id_seq OWNED BY public.app1_bom.id;
          public          admin    false    238            �            1259    16626    app1_bom_material_code    TABLE     �   CREATE TABLE public.app1_bom_material_code (
    id integer NOT NULL,
    bom_id integer NOT NULL,
    material_id integer NOT NULL
);
 *   DROP TABLE public.app1_bom_material_code;
       public         heap    admin    false            �            1259    16624    app1_bom_material_code_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_bom_material_code_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.app1_bom_material_code_id_seq;
       public          admin    false    241            �           0    0    app1_bom_material_code_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.app1_bom_material_code_id_seq OWNED BY public.app1_bom_material_code.id;
          public          admin    false    240            �            1259    16534    app1_calendar    TABLE     �   CREATE TABLE public.app1_calendar (
    id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    working boolean NOT NULL
);
 !   DROP TABLE public.app1_calendar;
       public         heap    admin    false            �            1259    16532    app1_calendar_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_calendar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.app1_calendar_id_seq;
       public          admin    false    219            �           0    0    app1_calendar_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.app1_calendar_id_seq OWNED BY public.app1_calendar.id;
          public          admin    false    218            �            1259    16542 	   app1_line    TABLE     c   CREATE TABLE public.app1_line (
    id integer NOT NULL,
    line character varying(3) NOT NULL
);
    DROP TABLE public.app1_line;
       public         heap    admin    false            �            1259    16540    app1_line_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.app1_line_id_seq;
       public          admin    false    221                        0    0    app1_line_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.app1_line_id_seq OWNED BY public.app1_line.id;
          public          admin    false    220            �            1259    16552    app1_material    TABLE     -  CREATE TABLE public.app1_material (
    id integer NOT NULL,
    code character varying(12) NOT NULL,
    "desc" character varying(35) NOT NULL,
    rate numeric(7,2) NOT NULL,
    uom character varying(3) NOT NULL,
    lead_time integer NOT NULL,
    classification character varying(10) NOT NULL
);
 !   DROP TABLE public.app1_material;
       public         heap    admin    false            �            1259    16550    app1_material_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_material_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.app1_material_id_seq;
       public          admin    false    223                       0    0    app1_material_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.app1_material_id_seq OWNED BY public.app1_material.id;
          public          admin    false    222            �            1259    16610 	   app1_plan    TABLE     �   CREATE TABLE public.app1_plan (
    id integer NOT NULL,
    date timestamp with time zone,
    plan_qty integer NOT NULL,
    line_id character varying(3),
    so_id integer
);
    DROP TABLE public.app1_plan;
       public         heap    admin    false            �            1259    16608    app1_plan_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.app1_plan_id_seq;
       public          admin    false    237                       0    0    app1_plan_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.app1_plan_id_seq OWNED BY public.app1_plan.id;
          public          admin    false    236            �            1259    16560    app1_product    TABLE     �  CREATE TABLE public.app1_product (
    id integer NOT NULL,
    code character varying(15) NOT NULL,
    "desc" character varying(60) NOT NULL,
    case_size integer,
    bulk_code character varying(7) NOT NULL,
    micro boolean,
    carton boolean,
    bus_category character varying(15),
    prod_category character varying(25) NOT NULL,
    gr_wt numeric(9,4),
    nt_wt numeric(9,4),
    plant character varying(4) NOT NULL,
    line_bulk character varying(25),
    des_code character varying(15)
);
     DROP TABLE public.app1_product;
       public         heap    admin    false            �            1259    16558    app1_product_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.app1_product_id_seq;
       public          admin    false    225                       0    0    app1_product_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.app1_product_id_seq OWNED BY public.app1_product.id;
          public          admin    false    224            �            1259    16602    app1_production    TABLE     �   CREATE TABLE public.app1_production (
    id integer NOT NULL,
    date date NOT NULL,
    shift character varying(1) NOT NULL,
    qty numeric(7,2) NOT NULL,
    doc_date date NOT NULL,
    code_id integer NOT NULL,
    line_id integer
);
 #   DROP TABLE public.app1_production;
       public         heap    admin    false            �            1259    16600    app1_production_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_production_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.app1_production_id_seq;
       public          admin    false    235                       0    0    app1_production_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.app1_production_id_seq OWNED BY public.app1_production.id;
          public          admin    false    234            �            1259    16594    app1_so    TABLE     �  CREATE TABLE public.app1_so (
    id integer NOT NULL,
    so character varying(25) NOT NULL,
    so_date date NOT NULL,
    so_del_date date NOT NULL,
    qty numeric(7,1) NOT NULL,
    closed boolean NOT NULL,
    act_disp_qty integer,
    act_disp_date date,
    rate numeric(5,2),
    currency character varying(3),
    customer character varying(35) NOT NULL,
    fgcode_id integer
);
    DROP TABLE public.app1_so;
       public         heap    admin    false            �            1259    16592    app1_so_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_so_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.app1_so_id_seq;
       public          admin    false    233                       0    0    app1_so_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.app1_so_id_seq OWNED BY public.app1_so.id;
          public          admin    false    232            �            1259    16586 
   app1_speed    TABLE     �   CREATE TABLE public.app1_speed (
    id integer NOT NULL,
    speed double precision NOT NULL,
    code_id character varying(15),
    line_id character varying(3)
);
    DROP TABLE public.app1_speed;
       public         heap    admin    false            �            1259    16584    app1_speed_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_speed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.app1_speed_id_seq;
       public          admin    false    231                       0    0    app1_speed_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.app1_speed_id_seq OWNED BY public.app1_speed.id;
          public          admin    false    230            �            1259    16578 
   app1_stock    TABLE     �   CREATE TABLE public.app1_stock (
    id integer NOT NULL,
    qty_released numeric(9,2) NOT NULL,
    qty_quality numeric(9,2) NOT NULL,
    uom character varying(3) NOT NULL,
    material_code_id integer
);
    DROP TABLE public.app1_stock;
       public         heap    admin    false            �            1259    16576    app1_stock_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.app1_stock_id_seq;
       public          admin    false    229                       0    0    app1_stock_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.app1_stock_id_seq OWNED BY public.app1_stock.id;
          public          admin    false    228            �            1259    16570    app1_stockfg    TABLE     �   CREATE TABLE public.app1_stockfg (
    id integer NOT NULL,
    qty_released numeric(9,2) NOT NULL,
    qty_quality numeric(9,2) NOT NULL,
    uom character varying(3) NOT NULL,
    material_code_id integer
);
     DROP TABLE public.app1_stockfg;
       public         heap    admin    false            �            1259    16568    app1_stockfg_id_seq    SEQUENCE     �   CREATE SEQUENCE public.app1_stockfg_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.app1_stockfg_id_seq;
       public          admin    false    227                       0    0    app1_stockfg_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.app1_stockfg_id_seq OWNED BY public.app1_stockfg.id;
          public          admin    false    226            �            1259    16414 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public         heap    admin    false            �            1259    16412    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public          admin    false    207            	           0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
          public          admin    false    206            �            1259    16424    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public         heap    admin    false            �            1259    16422    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public          admin    false    209            
           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
          public          admin    false    208            �            1259    16406    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public         heap    admin    false            �            1259    16404    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public          admin    false    205                       0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
          public          admin    false    204            �            1259    16432 	   auth_user    TABLE     �  CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
    DROP TABLE public.auth_user;
       public         heap    admin    false            �            1259    16442    auth_user_groups    TABLE        CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
 $   DROP TABLE public.auth_user_groups;
       public         heap    admin    false            �            1259    16440    auth_user_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.auth_user_groups_id_seq;
       public          admin    false    213                       0    0    auth_user_groups_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;
          public          admin    false    212            �            1259    16430    auth_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.auth_user_id_seq;
       public          admin    false    211                       0    0    auth_user_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;
          public          admin    false    210            �            1259    16450    auth_user_user_permissions    TABLE     �   CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
 .   DROP TABLE public.auth_user_user_permissions;
       public         heap    admin    false            �            1259    16448 !   auth_user_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.auth_user_user_permissions_id_seq;
       public          admin    false    215                       0    0 !   auth_user_user_permissions_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;
          public          admin    false    214            �            1259    16510    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public         heap    admin    false            �            1259    16508    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public          admin    false    217                       0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
          public          admin    false    216            �            1259    16396    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public         heap    admin    false            �            1259    16394    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public          admin    false    203                       0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
          public          admin    false    202            �            1259    16388    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public         heap    admin    false            �            1259    16386    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public          admin    false    201                       0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
          public          admin    false    200            �            1259    16760    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public         heap    admin    false            �            1259    16719    reversion_revision    TABLE     �   CREATE TABLE public.reversion_revision (
    id integer NOT NULL,
    date_created timestamp with time zone NOT NULL,
    comment text NOT NULL,
    user_id integer
);
 &   DROP TABLE public.reversion_revision;
       public         heap    admin    false            �            1259    16717    reversion_revision_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reversion_revision_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.reversion_revision_id_seq;
       public          admin    false    243                       0    0    reversion_revision_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.reversion_revision_id_seq OWNED BY public.reversion_revision.id;
          public          admin    false    242            �            1259    16730    reversion_version    TABLE     P  CREATE TABLE public.reversion_version (
    id integer NOT NULL,
    object_id character varying(191) NOT NULL,
    format character varying(255) NOT NULL,
    serialized_data text NOT NULL,
    object_repr text NOT NULL,
    content_type_id integer NOT NULL,
    revision_id integer NOT NULL,
    db character varying(191) NOT NULL
);
 %   DROP TABLE public.reversion_version;
       public         heap    admin    false            �            1259    16728    reversion_version_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reversion_version_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.reversion_version_id_seq;
       public          admin    false    245                       0    0    reversion_version_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.reversion_version_id_seq OWNED BY public.reversion_version.id;
          public          admin    false    244            �           2604    16621    app1_bom id    DEFAULT     j   ALTER TABLE ONLY public.app1_bom ALTER COLUMN id SET DEFAULT nextval('public.app1_bom_id_seq'::regclass);
 :   ALTER TABLE public.app1_bom ALTER COLUMN id DROP DEFAULT;
       public          admin    false    239    238    239            �           2604    16629    app1_bom_material_code id    DEFAULT     �   ALTER TABLE ONLY public.app1_bom_material_code ALTER COLUMN id SET DEFAULT nextval('public.app1_bom_material_code_id_seq'::regclass);
 H   ALTER TABLE public.app1_bom_material_code ALTER COLUMN id DROP DEFAULT;
       public          admin    false    240    241    241            �           2604    16537    app1_calendar id    DEFAULT     t   ALTER TABLE ONLY public.app1_calendar ALTER COLUMN id SET DEFAULT nextval('public.app1_calendar_id_seq'::regclass);
 ?   ALTER TABLE public.app1_calendar ALTER COLUMN id DROP DEFAULT;
       public          admin    false    218    219    219            �           2604    16545    app1_line id    DEFAULT     l   ALTER TABLE ONLY public.app1_line ALTER COLUMN id SET DEFAULT nextval('public.app1_line_id_seq'::regclass);
 ;   ALTER TABLE public.app1_line ALTER COLUMN id DROP DEFAULT;
       public          admin    false    221    220    221            �           2604    16555    app1_material id    DEFAULT     t   ALTER TABLE ONLY public.app1_material ALTER COLUMN id SET DEFAULT nextval('public.app1_material_id_seq'::regclass);
 ?   ALTER TABLE public.app1_material ALTER COLUMN id DROP DEFAULT;
       public          admin    false    222    223    223            �           2604    16613    app1_plan id    DEFAULT     l   ALTER TABLE ONLY public.app1_plan ALTER COLUMN id SET DEFAULT nextval('public.app1_plan_id_seq'::regclass);
 ;   ALTER TABLE public.app1_plan ALTER COLUMN id DROP DEFAULT;
       public          admin    false    237    236    237            �           2604    16563    app1_product id    DEFAULT     r   ALTER TABLE ONLY public.app1_product ALTER COLUMN id SET DEFAULT nextval('public.app1_product_id_seq'::regclass);
 >   ALTER TABLE public.app1_product ALTER COLUMN id DROP DEFAULT;
       public          admin    false    225    224    225            �           2604    16605    app1_production id    DEFAULT     x   ALTER TABLE ONLY public.app1_production ALTER COLUMN id SET DEFAULT nextval('public.app1_production_id_seq'::regclass);
 A   ALTER TABLE public.app1_production ALTER COLUMN id DROP DEFAULT;
       public          admin    false    234    235    235            �           2604    16597 
   app1_so id    DEFAULT     h   ALTER TABLE ONLY public.app1_so ALTER COLUMN id SET DEFAULT nextval('public.app1_so_id_seq'::regclass);
 9   ALTER TABLE public.app1_so ALTER COLUMN id DROP DEFAULT;
       public          admin    false    232    233    233            �           2604    16589    app1_speed id    DEFAULT     n   ALTER TABLE ONLY public.app1_speed ALTER COLUMN id SET DEFAULT nextval('public.app1_speed_id_seq'::regclass);
 <   ALTER TABLE public.app1_speed ALTER COLUMN id DROP DEFAULT;
       public          admin    false    231    230    231            �           2604    16581    app1_stock id    DEFAULT     n   ALTER TABLE ONLY public.app1_stock ALTER COLUMN id SET DEFAULT nextval('public.app1_stock_id_seq'::regclass);
 <   ALTER TABLE public.app1_stock ALTER COLUMN id DROP DEFAULT;
       public          admin    false    228    229    229            �           2604    16573    app1_stockfg id    DEFAULT     r   ALTER TABLE ONLY public.app1_stockfg ALTER COLUMN id SET DEFAULT nextval('public.app1_stockfg_id_seq'::regclass);
 >   ALTER TABLE public.app1_stockfg ALTER COLUMN id DROP DEFAULT;
       public          admin    false    226    227    227            �           2604    16417    auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public          admin    false    207    206    207            �           2604    16427    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public          admin    false    208    209    209            �           2604    16409    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public          admin    false    204    205    205            �           2604    16435    auth_user id    DEFAULT     l   ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);
 ;   ALTER TABLE public.auth_user ALTER COLUMN id DROP DEFAULT;
       public          admin    false    211    210    211            �           2604    16445    auth_user_groups id    DEFAULT     z   ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);
 B   ALTER TABLE public.auth_user_groups ALTER COLUMN id DROP DEFAULT;
       public          admin    false    212    213    213            �           2604    16453    auth_user_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);
 L   ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id DROP DEFAULT;
       public          admin    false    214    215    215            �           2604    16513    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public          admin    false    216    217    217            �           2604    16399    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public          admin    false    202    203    203            �           2604    16391    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public          admin    false    201    200    201            �           2604    16722    reversion_revision id    DEFAULT     ~   ALTER TABLE ONLY public.reversion_revision ALTER COLUMN id SET DEFAULT nextval('public.reversion_revision_id_seq'::regclass);
 D   ALTER TABLE public.reversion_revision ALTER COLUMN id DROP DEFAULT;
       public          admin    false    242    243    243            �           2604    16733    reversion_version id    DEFAULT     |   ALTER TABLE ONLY public.reversion_version ALTER COLUMN id SET DEFAULT nextval('public.reversion_version_id_seq'::regclass);
 C   ALTER TABLE public.reversion_version ALTER COLUMN id DROP DEFAULT;
       public          admin    false    245    244    245            �          0    16618    app1_bom 
   TABLE DATA           A   COPY public.app1_bom (id, qty, uom, active, code_id) FROM stdin;
    public          admin    false    239   2      �          0    16626    app1_bom_material_code 
   TABLE DATA           I   COPY public.app1_bom_material_code (id, bom_id, material_id) FROM stdin;
    public          admin    false    241   ;2      �          0    16534    app1_calendar 
   TABLE DATA           :   COPY public.app1_calendar (id, date, working) FROM stdin;
    public          admin    false    219   X2      �          0    16542 	   app1_line 
   TABLE DATA           -   COPY public.app1_line (id, line) FROM stdin;
    public          admin    false    221   u2      �          0    16552    app1_material 
   TABLE DATA           _   COPY public.app1_material (id, code, "desc", rate, uom, lead_time, classification) FROM stdin;
    public          admin    false    223   �2      �          0    16610 	   app1_plan 
   TABLE DATA           G   COPY public.app1_plan (id, date, plan_qty, line_id, so_id) FROM stdin;
    public          admin    false    237   �2      �          0    16560    app1_product 
   TABLE DATA           �   COPY public.app1_product (id, code, "desc", case_size, bulk_code, micro, carton, bus_category, prod_category, gr_wt, nt_wt, plant, line_bulk, des_code) FROM stdin;
    public          admin    false    225   �2      �          0    16602    app1_production 
   TABLE DATA           [   COPY public.app1_production (id, date, shift, qty, doc_date, code_id, line_id) FROM stdin;
    public          admin    false    235   ol      �          0    16594    app1_so 
   TABLE DATA           �   COPY public.app1_so (id, so, so_date, so_del_date, qty, closed, act_disp_qty, act_disp_date, rate, currency, customer, fgcode_id) FROM stdin;
    public          admin    false    233   �l      �          0    16586 
   app1_speed 
   TABLE DATA           A   COPY public.app1_speed (id, speed, code_id, line_id) FROM stdin;
    public          admin    false    231   ��      �          0    16578 
   app1_stock 
   TABLE DATA           Z   COPY public.app1_stock (id, qty_released, qty_quality, uom, material_code_id) FROM stdin;
    public          admin    false    229   ڳ      �          0    16570    app1_stockfg 
   TABLE DATA           \   COPY public.app1_stockfg (id, qty_released, qty_quality, uom, material_code_id) FROM stdin;
    public          admin    false    227   ��      �          0    16414 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          admin    false    207   �      �          0    16424    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          admin    false    209   1�      �          0    16406    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          admin    false    205   N�      �          0    16432 	   auth_user 
   TABLE DATA           �   COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
    public          admin    false    211   k�      �          0    16442    auth_user_groups 
   TABLE DATA           A   COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
    public          admin    false    213   ��      �          0    16450    auth_user_user_permissions 
   TABLE DATA           P   COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
    public          admin    false    215   ��      �          0    16510    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          admin    false    217   ´      �          0    16396    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          admin    false    203   ߴ      �          0    16388    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          admin    false    201   ��      �          0    16760    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          admin    false    246   �      �          0    16719    reversion_revision 
   TABLE DATA           P   COPY public.reversion_revision (id, date_created, comment, user_id) FROM stdin;
    public          admin    false    243   �      �          0    16730    reversion_version 
   TABLE DATA           �   COPY public.reversion_version (id, object_id, format, serialized_data, object_repr, content_type_id, revision_id, db) FROM stdin;
    public          admin    false    245   #�                 0    0    app1_bom_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.app1_bom_id_seq', 1, false);
          public          admin    false    238                       0    0    app1_bom_material_code_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.app1_bom_material_code_id_seq', 1, false);
          public          admin    false    240                       0    0    app1_calendar_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.app1_calendar_id_seq', 1, false);
          public          admin    false    218                       0    0    app1_line_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.app1_line_id_seq', 1, false);
          public          admin    false    220                       0    0    app1_material_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.app1_material_id_seq', 1, false);
          public          admin    false    222                       0    0    app1_plan_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.app1_plan_id_seq', 1, false);
          public          admin    false    236                       0    0    app1_product_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.app1_product_id_seq', 507, true);
          public          admin    false    224                       0    0    app1_production_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.app1_production_id_seq', 1, false);
          public          admin    false    234                       0    0    app1_so_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.app1_so_id_seq', 3844, true);
          public          admin    false    232                       0    0    app1_speed_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.app1_speed_id_seq', 1, false);
          public          admin    false    230                       0    0    app1_stock_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.app1_stock_id_seq', 1, false);
          public          admin    false    228                       0    0    app1_stockfg_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.app1_stockfg_id_seq', 1, false);
          public          admin    false    226                        0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public          admin    false    206            !           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public          admin    false    208            "           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 76, true);
          public          admin    false    204            #           0    0    auth_user_groups_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);
          public          admin    false    212            $           0    0    auth_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);
          public          admin    false    210            %           0    0 !   auth_user_user_permissions_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);
          public          admin    false    214            &           0    0    django_admin_log_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);
          public          admin    false    216            '           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 19, true);
          public          admin    false    202            (           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 20, true);
          public          admin    false    200            )           0    0    reversion_revision_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.reversion_revision_id_seq', 1, false);
          public          admin    false    242            *           0    0    reversion_version_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.reversion_version_id_seq', 1, false);
          public          admin    false    244                       2606    16698 N   app1_bom_material_code app1_bom_material_code_bom_id_material_id_838ceb9b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.app1_bom_material_code
    ADD CONSTRAINT app1_bom_material_code_bom_id_material_id_838ceb9b_uniq UNIQUE (bom_id, material_id);
 x   ALTER TABLE ONLY public.app1_bom_material_code DROP CONSTRAINT app1_bom_material_code_bom_id_material_id_838ceb9b_uniq;
       public            admin    false    241    241                       2606    16631 2   app1_bom_material_code app1_bom_material_code_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.app1_bom_material_code
    ADD CONSTRAINT app1_bom_material_code_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.app1_bom_material_code DROP CONSTRAINT app1_bom_material_code_pkey;
       public            admin    false    241                       2606    16623    app1_bom app1_bom_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.app1_bom
    ADD CONSTRAINT app1_bom_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.app1_bom DROP CONSTRAINT app1_bom_pkey;
       public            admin    false    239            �           2606    16539     app1_calendar app1_calendar_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.app1_calendar
    ADD CONSTRAINT app1_calendar_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.app1_calendar DROP CONSTRAINT app1_calendar_pkey;
       public            admin    false    219            �           2606    16549    app1_line app1_line_line_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.app1_line
    ADD CONSTRAINT app1_line_line_key UNIQUE (line);
 F   ALTER TABLE ONLY public.app1_line DROP CONSTRAINT app1_line_line_key;
       public            admin    false    221            �           2606    16547    app1_line app1_line_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.app1_line
    ADD CONSTRAINT app1_line_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.app1_line DROP CONSTRAINT app1_line_pkey;
       public            admin    false    221            �           2606    16557     app1_material app1_material_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.app1_material
    ADD CONSTRAINT app1_material_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.app1_material DROP CONSTRAINT app1_material_pkey;
       public            admin    false    223                       2606    16615    app1_plan app1_plan_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.app1_plan
    ADD CONSTRAINT app1_plan_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.app1_plan DROP CONSTRAINT app1_plan_pkey;
       public            admin    false    237            �           2606    16567 "   app1_product app1_product_code_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public.app1_product
    ADD CONSTRAINT app1_product_code_key UNIQUE (code);
 L   ALTER TABLE ONLY public.app1_product DROP CONSTRAINT app1_product_code_key;
       public            admin    false    225            �           2606    16565    app1_product app1_product_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.app1_product
    ADD CONSTRAINT app1_product_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.app1_product DROP CONSTRAINT app1_product_pkey;
       public            admin    false    225                       2606    16607 $   app1_production app1_production_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.app1_production
    ADD CONSTRAINT app1_production_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.app1_production DROP CONSTRAINT app1_production_pkey;
       public            admin    false    235                       2606    16599    app1_so app1_so_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.app1_so
    ADD CONSTRAINT app1_so_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.app1_so DROP CONSTRAINT app1_so_pkey;
       public            admin    false    233            
           2606    16591    app1_speed app1_speed_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.app1_speed
    ADD CONSTRAINT app1_speed_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.app1_speed DROP CONSTRAINT app1_speed_pkey;
       public            admin    false    231                       2606    16583    app1_stock app1_stock_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.app1_stock
    ADD CONSTRAINT app1_stock_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.app1_stock DROP CONSTRAINT app1_stock_pkey;
       public            admin    false    229                       2606    16575    app1_stockfg app1_stockfg_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.app1_stockfg
    ADD CONSTRAINT app1_stockfg_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.app1_stockfg DROP CONSTRAINT app1_stockfg_pkey;
       public            admin    false    227            �           2606    16715    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            admin    false    207            �           2606    16466 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            admin    false    209    209            �           2606    16429 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            admin    false    209            �           2606    16419    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            admin    false    207            �           2606    16457 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            admin    false    205    205            �           2606    16411 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            admin    false    205            �           2606    16447 &   auth_user_groups auth_user_groups_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
       public            admin    false    213            �           2606    16481 @   auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);
 j   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
       public            admin    false    213    213            �           2606    16437    auth_user auth_user_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
       public            admin    false    211            �           2606    16455 :   auth_user_user_permissions auth_user_user_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
       public            admin    false    215            �           2606    16495 Y   auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
       public            admin    false    215    215            �           2606    16712     auth_user auth_user_username_key 
   CONSTRAINT     _   ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);
 J   ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
       public            admin    false    211            �           2606    16519 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            admin    false    217            �           2606    16403 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            admin    false    203    203            �           2606    16401 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            admin    false    203            �           2606    16393 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            admin    false    201            ,           2606    16767 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public            admin    false    246            "           2606    16727 *   reversion_revision reversion_revision_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.reversion_revision
    ADD CONSTRAINT reversion_revision_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.reversion_revision DROP CONSTRAINT reversion_revision_pkey;
       public            admin    false    243            &           2606    16740 J   reversion_version reversion_version_db_content_type_id_objec_b2c54f65_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.reversion_version
    ADD CONSTRAINT reversion_version_db_content_type_id_objec_b2c54f65_uniq UNIQUE (db, content_type_id, object_id, revision_id);
 t   ALTER TABLE ONLY public.reversion_version DROP CONSTRAINT reversion_version_db_content_type_id_objec_b2c54f65_uniq;
       public            admin    false    245    245    245    245            (           2606    16738 (   reversion_version reversion_version_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.reversion_version
    ADD CONSTRAINT reversion_version_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.reversion_version DROP CONSTRAINT reversion_version_pkey;
       public            admin    false    245                       1259    16696    app1_bom_code_id_4d932efe    INDEX     Q   CREATE INDEX app1_bom_code_id_4d932efe ON public.app1_bom USING btree (code_id);
 -   DROP INDEX public.app1_bom_code_id_4d932efe;
       public            admin    false    239                       1259    16709 &   app1_bom_material_code_bom_id_21c00c56    INDEX     k   CREATE INDEX app1_bom_material_code_bom_id_21c00c56 ON public.app1_bom_material_code USING btree (bom_id);
 :   DROP INDEX public.app1_bom_material_code_bom_id_21c00c56;
       public            admin    false    241                       1259    16710 +   app1_bom_material_code_material_id_ab92af0d    INDEX     u   CREATE INDEX app1_bom_material_code_material_id_ab92af0d ON public.app1_bom_material_code USING btree (material_id);
 ?   DROP INDEX public.app1_bom_material_code_material_id_ab92af0d;
       public            admin    false    241            �           1259    16632    app1_line_line_4bd52f02_like    INDEX     f   CREATE INDEX app1_line_line_4bd52f02_like ON public.app1_line USING btree (line varchar_pattern_ops);
 0   DROP INDEX public.app1_line_line_4bd52f02_like;
       public            admin    false    221                       1259    16688    app1_plan_line_id_be7906b7    INDEX     S   CREATE INDEX app1_plan_line_id_be7906b7 ON public.app1_plan USING btree (line_id);
 .   DROP INDEX public.app1_plan_line_id_be7906b7;
       public            admin    false    237                       1259    16689    app1_plan_line_id_be7906b7_like    INDEX     l   CREATE INDEX app1_plan_line_id_be7906b7_like ON public.app1_plan USING btree (line_id varchar_pattern_ops);
 3   DROP INDEX public.app1_plan_line_id_be7906b7_like;
       public            admin    false    237                       1259    16690    app1_plan_so_id_aebe1fde    INDEX     O   CREATE INDEX app1_plan_so_id_aebe1fde ON public.app1_plan USING btree (so_id);
 ,   DROP INDEX public.app1_plan_so_id_aebe1fde;
       public            admin    false    237            �           1259    16633    app1_product_code_43ed5e4c_like    INDEX     l   CREATE INDEX app1_product_code_43ed5e4c_like ON public.app1_product USING btree (code varchar_pattern_ops);
 3   DROP INDEX public.app1_product_code_43ed5e4c_like;
       public            admin    false    225                       1259    16676     app1_production_code_id_3d973f07    INDEX     _   CREATE INDEX app1_production_code_id_3d973f07 ON public.app1_production USING btree (code_id);
 4   DROP INDEX public.app1_production_code_id_3d973f07;
       public            admin    false    235                       1259    16677     app1_production_line_id_b78fc4ca    INDEX     _   CREATE INDEX app1_production_line_id_b78fc4ca ON public.app1_production USING btree (line_id);
 4   DROP INDEX public.app1_production_line_id_b78fc4ca;
       public            admin    false    235                       1259    16665    app1_so_fgcode_id_fed4295f    INDEX     S   CREATE INDEX app1_so_fgcode_id_fed4295f ON public.app1_so USING btree (fgcode_id);
 .   DROP INDEX public.app1_so_fgcode_id_fed4295f;
       public            admin    false    233                       1259    16656    app1_speed_code_id_61987cfa    INDEX     U   CREATE INDEX app1_speed_code_id_61987cfa ON public.app1_speed USING btree (code_id);
 /   DROP INDEX public.app1_speed_code_id_61987cfa;
       public            admin    false    231                       1259    16657     app1_speed_code_id_61987cfa_like    INDEX     n   CREATE INDEX app1_speed_code_id_61987cfa_like ON public.app1_speed USING btree (code_id varchar_pattern_ops);
 4   DROP INDEX public.app1_speed_code_id_61987cfa_like;
       public            admin    false    231                       1259    16658    app1_speed_line_id_fcb14b22    INDEX     U   CREATE INDEX app1_speed_line_id_fcb14b22 ON public.app1_speed USING btree (line_id);
 /   DROP INDEX public.app1_speed_line_id_fcb14b22;
       public            admin    false    231                       1259    16659     app1_speed_line_id_fcb14b22_like    INDEX     n   CREATE INDEX app1_speed_line_id_fcb14b22_like ON public.app1_speed USING btree (line_id varchar_pattern_ops);
 4   DROP INDEX public.app1_speed_line_id_fcb14b22_like;
       public            admin    false    231                       1259    16645 $   app1_stock_material_code_id_f494625c    INDEX     g   CREATE INDEX app1_stock_material_code_id_f494625c ON public.app1_stock USING btree (material_code_id);
 8   DROP INDEX public.app1_stock_material_code_id_f494625c;
       public            admin    false    229            �           1259    16639 &   app1_stockfg_material_code_id_8b16a66b    INDEX     k   CREATE INDEX app1_stockfg_material_code_id_8b16a66b ON public.app1_stockfg USING btree (material_code_id);
 :   DROP INDEX public.app1_stockfg_material_code_id_8b16a66b;
       public            admin    false    227            �           1259    16716    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            admin    false    207            �           1259    16477 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            admin    false    209            �           1259    16478 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            admin    false    209            �           1259    16463 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            admin    false    205            �           1259    16493 "   auth_user_groups_group_id_97559544    INDEX     c   CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);
 6   DROP INDEX public.auth_user_groups_group_id_97559544;
       public            admin    false    213            �           1259    16492 !   auth_user_groups_user_id_6a12ed8b    INDEX     a   CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);
 5   DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
       public            admin    false    213            �           1259    16507 1   auth_user_user_permissions_permission_id_1fbb5f2c    INDEX     �   CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);
 E   DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
       public            admin    false    215            �           1259    16506 +   auth_user_user_permissions_user_id_a95ead1b    INDEX     u   CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);
 ?   DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
       public            admin    false    215            �           1259    16713     auth_user_username_6821ab7c_like    INDEX     n   CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);
 4   DROP INDEX public.auth_user_username_6821ab7c_like;
       public            admin    false    211            �           1259    16530 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            admin    false    217            �           1259    16531 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            admin    false    217            *           1259    16769 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public            admin    false    246            -           1259    16768 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public            admin    false    246                        1259    16746 (   reversion_revision_date_created_96f7c20c    INDEX     o   CREATE INDEX reversion_revision_date_created_96f7c20c ON public.reversion_revision USING btree (date_created);
 <   DROP INDEX public.reversion_revision_date_created_96f7c20c;
       public            admin    false    243            #           1259    16747 #   reversion_revision_user_id_17095f45    INDEX     e   CREATE INDEX reversion_revision_user_id_17095f45 ON public.reversion_revision USING btree (user_id);
 7   DROP INDEX public.reversion_revision_user_id_17095f45;
       public            admin    false    243            $           1259    16758 *   reversion_version_content_type_id_7d0ff25c    INDEX     s   CREATE INDEX reversion_version_content_type_id_7d0ff25c ON public.reversion_version USING btree (content_type_id);
 >   DROP INDEX public.reversion_version_content_type_id_7d0ff25c;
       public            admin    false    245            )           1259    16759 &   reversion_version_revision_id_af9f6a9d    INDEX     k   CREATE INDEX reversion_version_revision_id_af9f6a9d ON public.reversion_version USING btree (revision_id);
 :   DROP INDEX public.reversion_version_revision_id_af9f6a9d;
       public            admin    false    245            @           2606    16691 5   app1_bom app1_bom_code_id_4d932efe_fk_app1_product_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_bom
    ADD CONSTRAINT app1_bom_code_id_4d932efe_fk_app1_product_id FOREIGN KEY (code_id) REFERENCES public.app1_product(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.app1_bom DROP CONSTRAINT app1_bom_code_id_4d932efe_fk_app1_product_id;
       public          admin    false    239    225    3070            A           2606    16699 L   app1_bom_material_code app1_bom_material_code_bom_id_21c00c56_fk_app1_bom_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_bom_material_code
    ADD CONSTRAINT app1_bom_material_code_bom_id_21c00c56_fk_app1_bom_id FOREIGN KEY (bom_id) REFERENCES public.app1_bom(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.app1_bom_material_code DROP CONSTRAINT app1_bom_material_code_bom_id_21c00c56_fk_app1_bom_id;
       public          admin    false    241    239    3097            B           2606    16704 V   app1_bom_material_code app1_bom_material_code_material_id_ab92af0d_fk_app1_material_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_bom_material_code
    ADD CONSTRAINT app1_bom_material_code_material_id_ab92af0d_fk_app1_material_id FOREIGN KEY (material_id) REFERENCES public.app1_material(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.app1_bom_material_code DROP CONSTRAINT app1_bom_material_code_material_id_ab92af0d_fk_app1_material_id;
       public          admin    false    241    223    3065            >           2606    16678 6   app1_plan app1_plan_line_id_be7906b7_fk_app1_line_line    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_plan
    ADD CONSTRAINT app1_plan_line_id_be7906b7_fk_app1_line_line FOREIGN KEY (line_id) REFERENCES public.app1_line(line) DEFERRABLE INITIALLY DEFERRED;
 `   ALTER TABLE ONLY public.app1_plan DROP CONSTRAINT app1_plan_line_id_be7906b7_fk_app1_line_line;
       public          admin    false    237    221    3061            ?           2606    16683 0   app1_plan app1_plan_so_id_aebe1fde_fk_app1_so_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_plan
    ADD CONSTRAINT app1_plan_so_id_aebe1fde_fk_app1_so_id FOREIGN KEY (so_id) REFERENCES public.app1_so(id) DEFERRABLE INITIALLY DEFERRED;
 Z   ALTER TABLE ONLY public.app1_plan DROP CONSTRAINT app1_plan_so_id_aebe1fde_fk_app1_so_id;
       public          admin    false    237    233    3085            <           2606    16666 C   app1_production app1_production_code_id_3d973f07_fk_app1_product_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_production
    ADD CONSTRAINT app1_production_code_id_3d973f07_fk_app1_product_id FOREIGN KEY (code_id) REFERENCES public.app1_product(id) DEFERRABLE INITIALLY DEFERRED;
 m   ALTER TABLE ONLY public.app1_production DROP CONSTRAINT app1_production_code_id_3d973f07_fk_app1_product_id;
       public          admin    false    225    235    3070            =           2606    16671 @   app1_production app1_production_line_id_b78fc4ca_fk_app1_line_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_production
    ADD CONSTRAINT app1_production_line_id_b78fc4ca_fk_app1_line_id FOREIGN KEY (line_id) REFERENCES public.app1_line(id) DEFERRABLE INITIALLY DEFERRED;
 j   ALTER TABLE ONLY public.app1_production DROP CONSTRAINT app1_production_line_id_b78fc4ca_fk_app1_line_id;
       public          admin    false    235    221    3063            ;           2606    16660 5   app1_so app1_so_fgcode_id_fed4295f_fk_app1_product_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_so
    ADD CONSTRAINT app1_so_fgcode_id_fed4295f_fk_app1_product_id FOREIGN KEY (fgcode_id) REFERENCES public.app1_product(id) DEFERRABLE INITIALLY DEFERRED;
 _   ALTER TABLE ONLY public.app1_so DROP CONSTRAINT app1_so_fgcode_id_fed4295f_fk_app1_product_id;
       public          admin    false    225    3070    233            9           2606    16646 ;   app1_speed app1_speed_code_id_61987cfa_fk_app1_product_code    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_speed
    ADD CONSTRAINT app1_speed_code_id_61987cfa_fk_app1_product_code FOREIGN KEY (code_id) REFERENCES public.app1_product(code) DEFERRABLE INITIALLY DEFERRED;
 e   ALTER TABLE ONLY public.app1_speed DROP CONSTRAINT app1_speed_code_id_61987cfa_fk_app1_product_code;
       public          admin    false    231    225    3068            :           2606    16651 8   app1_speed app1_speed_line_id_fcb14b22_fk_app1_line_line    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_speed
    ADD CONSTRAINT app1_speed_line_id_fcb14b22_fk_app1_line_line FOREIGN KEY (line_id) REFERENCES public.app1_line(line) DEFERRABLE INITIALLY DEFERRED;
 b   ALTER TABLE ONLY public.app1_speed DROP CONSTRAINT app1_speed_line_id_fcb14b22_fk_app1_line_line;
       public          admin    false    3061    221    231            8           2606    16640 C   app1_stock app1_stock_material_code_id_f494625c_fk_app1_material_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_stock
    ADD CONSTRAINT app1_stock_material_code_id_f494625c_fk_app1_material_id FOREIGN KEY (material_code_id) REFERENCES public.app1_material(id) DEFERRABLE INITIALLY DEFERRED;
 m   ALTER TABLE ONLY public.app1_stock DROP CONSTRAINT app1_stock_material_code_id_f494625c_fk_app1_material_id;
       public          admin    false    223    229    3065            7           2606    16634 F   app1_stockfg app1_stockfg_material_code_id_8b16a66b_fk_app1_product_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.app1_stockfg
    ADD CONSTRAINT app1_stockfg_material_code_id_8b16a66b_fk_app1_product_id FOREIGN KEY (material_code_id) REFERENCES public.app1_product(id) DEFERRABLE INITIALLY DEFERRED;
 p   ALTER TABLE ONLY public.app1_stockfg DROP CONSTRAINT app1_stockfg_material_code_id_8b16a66b_fk_app1_product_id;
       public          admin    false    225    227    3070            0           2606    16472 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          admin    false    209    205    3024            /           2606    16467 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          admin    false    209    3029    207            .           2606    16458 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          admin    false    205    3019    203            2           2606    16487 D   auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 n   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
       public          admin    false    207    3029    213            1           2606    16482 B   auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
       public          admin    false    3037    211    213            4           2606    16501 S   auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
       public          admin    false    215    205    3024            3           2606    16496 V   auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
       public          admin    false    3037    215    211            5           2606    16520 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          admin    false    203    217    3019            6           2606    16525 B   django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
       public          admin    false    217    211    3037            C           2606    16741 F   reversion_revision reversion_revision_user_id_17095f45_fk_auth_user_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.reversion_revision
    ADD CONSTRAINT reversion_revision_user_id_17095f45_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;
 p   ALTER TABLE ONLY public.reversion_revision DROP CONSTRAINT reversion_revision_user_id_17095f45_fk_auth_user_id;
       public          admin    false    211    243    3037            D           2606    16748 I   reversion_version reversion_version_content_type_id_7d0ff25c_fk_django_co    FK CONSTRAINT     �   ALTER TABLE ONLY public.reversion_version
    ADD CONSTRAINT reversion_version_content_type_id_7d0ff25c_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 s   ALTER TABLE ONLY public.reversion_version DROP CONSTRAINT reversion_version_content_type_id_7d0ff25c_fk_django_co;
       public          admin    false    3019    203    245            E           2606    16753 Q   reversion_version reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.reversion_version
    ADD CONSTRAINT reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id FOREIGN KEY (revision_id) REFERENCES public.reversion_revision(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.reversion_version DROP CONSTRAINT reversion_version_revision_id_af9f6a9d_fk_reversion_revision_id;
       public          admin    false    3106    245    243            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x����v"9����)t��ƫtJ���ܥ1`��x wuךʦ0S������G�W�#Bʳ2�ݫ�˅S|!)�B!��_K������a���7����i������eq<-�~�ix�q�O7N��v���F�O�k��lX�s��������%�ƿ�TI��) j���9`֛�u_?-�>[m�Ǉ�$pNv��.���#kL����!6�<ݱ4D*��6m�p4b2���pݛ1��Ƴ3��cd��M��Z�R5������?���C��ړ�?F��Kv7e�;m�w��5>�&ELJ�/���M���.Є���:�&<NxM5(-nY!����k��j��#����>��t����;,[Ʊ��~,ɯA�����)Ka� ���P, 7=ń��c
	HRl9Ӳ]�!�	)d��Dy����~Pt�ՐF���@���j`�����~}ς�G�
�3��ϡ~� ���&`�%��c@��	nf�t�܆���p��K�9����yJv3>C'��ٹ�q��çv�69캾�v�7�O{�[�=L�Û��z��=�K6`����n^�QV/6zy�֬�'�L�<(��&�5�{��]>��g����mu��GhhV�]nq��5�g�s��M��J��L�Jp���\4��1p������"m�����wA� 3������`�2+0e�.*��`�����֝t'!�~��{Svߛw�o���OfO>�|��9�X0T�,�N�l�V3��jVm�J!�#�W@O{��O�N'����aL�О}BtV������^���	�q�Q-��w�t�SP�Z��S&�|,�.��b�"\��9�m��HI�z�q�d��ç��������\Zlt:t
C�B�J�lH[��}��`��?Ma��>��mF����:A��֤3v��w{W9���GbSp��Q��	�-���Ԇ'V��e�>�wWj�rut���d�d ?�3�ceC��Xy��V5�]?#xR�6�m�������U�z:m���q�g�x���s[j�M�(���e\���r^�5�\�H���[%m�-�\rn���qS������-^�<�Ln�7�l
������m�߃3�?,�ޝX��u��
\�/+�ÜJ�RJI����9��a�I.����/��d7Ӈq{2��^oLo �*��t̯@Pz�^!0�`�~�a�Q�BD������b�R	<5= �g��q$ۢ��6ѽ�螦����cz���@��u�9�7�BV��7(�7��o �|S`�O���
�˪����&�0ɟ���E~��@����>�{t�ڪ�s�U��i3t���j�	j�F��b���æ-5��{`�Y�0��n�M[�jr��PX��쟩�>j�H��{��i�GtS�#zT�Jv����k����� �����\��B�.��i+���x�ڬ�Y��GroR�ت�W���"5+��gRه~/!��V.�kTy2�1�3��I�j]+ܭU�W�p��B�-.�/48��48W58G��2���F�G���X�5�5�ڕ���yu�R���`ʴN3G9���t�2~�D��O	�UN��{Y�n&/���t��J؉y/��~.Q&;�%�ݙ�\��1�}S��$�}+��M�sA�'�Ԏ-�U�iTOW�z�ٕ��ɟVS�Ĵ��;We�/Q6�u��8afǮ��-.fb+�V��#[��8��˛Z�t��h�.�72��L&�i�?�V�]�b�k����S+w�;֟���� �b0h��j��p�B��M���9�H�~��p�ok/^z${@GӇF����u��~T���^-���>X���j�
n�"�?H��緺$nu��֔h�h�z{�zy<�ŉ=.��q[��G���~C��剗G�v(VU��a�BK��c�mC,��I4t>:uj
q}x=>��ק���ȺϋC��_�h���#k�s�+vקUI,Xg炼�
�t-ƍ _w��=.�!�����V �,:�f�Ӿ�[����N�ζ������9�jh�e�эr���l ��Kτ�2u�w8l����t�؁sc�=�n8�����|�ǕH6��G=x��z�za�}wk}آ��2`�][�=y6ؓ��`q�����	��),�Ai���:�.m׏_!������0����f������2Tە��/���(��#��JE�ܮ$;L5r[���U��n@3�`���)��U�}�S�J�_X(` çM��7��덝�z�[��pwZ?.��O?� �o�"�-C���a�ށ��i�h�<)��[�d��6��;\�O�'�5+�%j�Iє+J��h���[v;��������g�s���\�v�i����5��؇����`�d��	�-x�T��Bu�ı�m+@��Ј��e��m�,>�����ZD�Z��w��u���v7Zu��ʔ�ȕ�:�ss����MO�A5����!XPֽ��	��]?W��M^])t��F}��xM�XW��q����JG������`����u�{O�b��5v�`�QM�!�@,��܈m_/������4�M�SQe"l)��5R�7S��.Qy%}!#���	�ԩ�~x^����n��#��f�CX_ˊ�~�7'�&բP\j�Ї~���.w�<��ʼ��B�q�Z��?s>=J�L��N܄QZ��j4�g����I�sݤ�Ѫ��%h[��m�zL�KY�Zbk�۵�*�K�b-tz
n��Gs�9��9��,G��٠��H(dl�&F)�3�(b}�����������m��p�A�6Z-{K�"Xӧ	�p���v�<~[|��/֝ݰ�y�wO��̱`�R�'�F��\�R�Jq���8��nL.��DԻ��H�I3F��JҌ��(��U��gxP���~.2�g�RT�(���\4��֐�K�B
���R2��"	��A؁�!��m`]�k�2�m�b/��/j_������?'�Yp����"�ڲ�-
�-�c,nɜ�*��Ҫ%sZ�`�3[<��5�ŠD
��������=�Y���L�dS�Z/�Q���V� ��e��0�'>�¿��6�lt��a? ���W�f@����w��Q���v}\���fd�[��<�z6a��Wf��v��O!g������b�n�����H����VA��:F���d^�,g:�2�}��u�'��
�\qͲ���Ic���rn���M�R����dj�穹�AS��"5���s?�U�Mj���iF�߃h�q�,��������}wF����rN���XFk
 �	�����[�x{<��N5P���P5!����r��4�m�M�⩏����iq�;�^
[!P�t����/�)���krj$�P�_�����gݚ�	�h*p�2�V��)��J�i�@a�qk��4�ɹ�iDn�er�R�ld&���:�:�j�cZ(4��������352G5:"�U'�ˣ���D�|n]�f����L���o&��ϫ��n}<��=�{�H(c�ƞd�H�_a�.$��g�������'���]*��K�^ 4m�D��)+k�u4�p�� @�S4��Ѵ��d�%ݤd6�0��`��y���_QX1Έڞ'T�����4r$�KN�p+�p-��Z���%�Z��R}f�ڥ�:���&�F�I7�2�pa,�;���5�F6G�(t7G�0:u�C�ɠ�2-G=��j�^�[/<Y#/6���g�)jT��(4 �u}h�PW��;�B+��h�E����a[)�ݓ'Z �vϿA:[ۡ����!�M�X��Ui�N8m�2>Af��Z�Y�1����V��`���Z�ݱ�}?6KFnig�@'U��:��ư�]N�F	kڒ�= �|�w�( n�ܘv��7oy�P,��q8N���ӂ�p��K������b,
<�N@�F�3PP��)�1��RX��2�1�=
���h
{i]wf���+@��v(�QP��eP�qT�$�*��[{&�u�R\�wy`���^����t�o��z.�s��d�K�=ݏ
�]|g�������A�����    iy8���4��u*���4g߷�[Ȥ�K��j�ފ"~���?,6�aPF*O�d��E���q}x8�y:��n't^�k�=���������z�<��s���~����z��t�ZI����(/�Q�j�)����qiG�}7��f�S���#��K�I(S��7O�BϰS��-yۍb˘��)A(X>����@/vO���N��1�N�G'�'>Q:X:������S[}�
+�5s/���~��
��b$���J�jb�*�j"�B59��;��΀ z�d�]o��%�
V-|z���W\n^�XQ�x >:�Cr�Yg֙���R\���dÐ����2�2<_IĠTYH��$JI���m9*������w6�(򣯳Dg�;:��j,����N14ӳh�*Ȟ���@Ƽ�o {>��R�qPho�]n�Ro,6��4k�A�E���k	w0�j8d��`�HA�zE�~
�F���Ut�e��g����^m���١ ��� pMe��5z�qo4ʤ��P��f<<�_��P�2١ ��i:�^F��AI�It�@t(H���48ݹz���ؼn��U�&��j�����,�^�(�����0�1�����=-$�g�$���-<�YsK ��;�s��$CD�^���m����� p%�Ǌ�Qx
 G�����u"��萵\1��xun�w�ta����
��zc�0��S���;&f�ߨ�ض����p!G��f�x|f���G� oJ��:��f����c�$��b�u�B"ر1ʇ�l���d�\0"m1U
�޳��f�C� �/����iyjȀ��a��B8Hat�ؒP���Va���4���
�W
�LX�m�	�������P����a�:����ԁ/�2"�O�k����v	nu][�T�E�@��|��
ꗙ+��]UV�nVڭ��R3�Kt]Ӵ�+U_H.Qu�̤i�֍Zqa��8|QQ�,n��*��-�
���!��j����#�-F	2���P	m�HL!��d��xҭ�L�5�X�A�,��ԇ0L�L�]�u�S�%�B�:����J��n@������l�~h%8-�Ǌ���$�[�*ZV�J�O�*�M5��o�6�.������C�*�ТR��JMC��ݫ���Z�h�Ԫ$zh)���edq�WJ��E�ڱ����;H��-� da}'F�b�^��eOQ�E⢋�k�j�.��I��i��2������Bu�BQ �U'�!��7r�n�ٛ.�]�q�`���x�oc��ST���gZ��~�$#�������\#�_��T��DΌ�I�%BJ%d�5��J
��
3�H��OI��J���h\�H� �2f������f��0%'&�L�f�P�z/�PI݆JDU���܋u���nB%�d�Lk��ڔ�6� �~��S�����t�^�Nl�_O��N�K��͆ScJ�"�u*f�ՠ&e%���Mk�$p�U
�5B����HW#�Y�ʳ��/+$H\V��cӡ��.!��T��;9F��~�^šX�<^s<�[LݫI�Uf(0a�_5���(l��v��Â��ö�n?��˚R���L��^,,�<�E�J�����n�u�7b�Xe�T³2�l�;�����h�l��-�+��(p*R{4+�+,�I���W��-N�������ϸ ��h�<a������v��g�h�ԁ������Fb�p�gQ�Jӓ�s`�d���Ջ�]t}�'��f}|a��w�������?lǲG�3����CI���w0&Ma�HXdt�M�W�p����,d���f��=�~�C�V	��*-sa6M� <�PX�� �짘�'�h�Sp�c�bsX��H��IR_Q��Qe%�_��6�`�- $Y%Q&�x�����M~p�Ro�R()���%Rf����HX,�P���L��SkJ�r�����sNGY���Kl����`��P�����P@������<,���,��C�����<�Q�Z�0.�vC0(`� ��B��9tN�S�J�/�֎�m:�K��e	0:$���d[=5�p��y���i���$�Z�����,%=o��t���q�t����ȼ8�Q,l� P�w�أ�)m^ʚG�H娑���0ʙ�g�sb��eb��$brg�<�����u��R1E���j�O��ٰwZ���h�R�G�vg=36��Y/�K�"��U���X{�c����O2��qM=��^4(����ĥ~"�.��4.���h2E�+4E3��2���X�-5�nq3M�K�U�\�|&�0yp�K.�,_�yXR,_	�T}�m+5��W_z��b3�64���l���J͌Vy�^4X�"�˫5�S�e9�^��vƤٔs�Rk�g���r���|n�N��~���-N�ݪ����1��揃���op<�"��q<.�}q�c�����A� ���e�e�xzf����p���J��&^�5��a�J��V"B�HF�62��|����E,x����iq���
���CvN���w���l�nٴ7����x2���r�F2s�=��`�ݥ9�@)��r�6����eU@<�W�'� �g�� ���E�H����lj~�"�5�kk�UM��f| �h~����\�#\���s�Z��X�����U�	�+-�O�͚�O_�G<�"����ڄ��(��ʨ�Z�ԧ�
*lۍ�-�+�_?U�<6_��^?}����u��S}cK�V�-�CA�*`[F��#�l�؜�����J�4P�.(
�a��q�W҇�v4:��":�]��NnM:�i;ik,7`�������a�s�@�r���~A�/���bcPz[H���k���VP�"xQmk�EV�c�~��D�!1W����{�j5��x��@	���"�1�v�{}a���o�]���\��ߩCW��'<��E8(h7*�
�Æc/�`��!��
��ۑo1x�O�z��v�ɿD�¢s_��KX�%(���4�j�qvu��Cg`��'��?1W��cX"~�5�x���cp�\�=�� �W�ǘ���<�D*t��w���m 0 ӵ~�.n��Oݝ��	�y��?YK�M{���^�$�����?s�ׁ��"ٵ�!��4|
l'��;��Jj縉T]�Qm�@�K���o�=&�(��(��@�M�}1'�ô���l�;��7h[_&��A�� h�ŕ~,�+���d���/)p;ޠ-���P����	�9\ ����aSP�7�ݼ�t�vӶ�ѥRc�~���K�v���m��pA��o����Pb2eﯶ�����ָc�ܚR<[ E<S�wp}'[�}��{�3����K�f��Z�y\S��q�Dl
�����xo vM��-�����-��¼�g?o�z��șl3��@����tAyR��B_h�^V!=v3���ŷ��� ��F9����T�/5�y�&Q�{=�n�@A�:��xC���=�l�|��z| M�j� �|�����Z��V�b�쯐�ڽ_{�P�y/�{�\k�*ڽn�+j�W�Z�=}hQ��Cl�^��踻���n����i���^����Cw#�uJ�:�L8`�p�k
J���w8��V-�koT{`�l8�6��nUt6��VQ?�[z=/0t4��2��{.�ݝ�3��Ex����<�X���D�pJC'�-���+EG�6/$�;_����;zX/mo�dXO;R��9��n��2�9(HmN��ܿ�jA�Ϯ8���e-D�^�.E�ζ��ڻKl��
Y3s�^T���m�xx��C	i�H���-��5�PЗ�&/���-����|?�� �W:^o�-q�u�k����8�A������ 	h���^�n���m�mP~4uPz?k�`���&vz���. چ1��`����ʑՕƑU����Z�6��C����}�ԭmx%����0R��#����m���l�6:��ɒ���h��Õ�}�jۚl�Lgt6^��|'Qx��oS��Tݞ�_f���*w�T�f�x�>'6-Ǟp��-~�w�������;Z���!ۛ��?!�O7T>�3 ���q�q��p�e��    �Щ�f��.J�o�5>�(��,I^�w<Q�
���u�8�&�+L>&� E/|,�^�!0��nC���?X�5�8�m����]��\E�jC�o��������:��DN��n�,�L�'�j����ص6s齖d���BEp�C�56��IV2���(j@{�k	�0�N�z�_�x8��g��[��J�''?����T��{���	U�L���@(4��h��]E)Zjɼ8�b!F)s9�}���j����yl�`Q��M	Tj�;Tc�Z��6J���܎�r��}M�y���~Ȅl��ig���7����7�4�Vߠ��AD�is)���f�	%�W{�-:��sq ���'���N��
��^��P�'��󢋚4<=���}P;^ִ�5���$���]M������2����=NʄG������d���l�,���Qޚ�^���)�����TZ �U^V��\�K�n!s��S�S&,���|���ʱ^�%���	����$c>;-_Q]�]�Juj�l�=%
۸�E����k�I���+������^�G/@{���}����;��w��e*��N�R)�=��/�W��N����dE�:Y�⢱���J3Rߊ���'�5t�3cƢ�xw�h�R@fc�6f-�-�����7��N�]��sМд���U�Q8�N`��;놿����d�S�:���n�ҷ�A����x��9P��L�9d!�ix-Y'$>���Mq��%�80�����X�D�^����f�9����qo��b�X�6p�4�.*�0�%��"g]MN)��lPt���)#��g���)4+g�AU�$�1��Y�Ԭ���YiM�tc:�jjR>I*53��4x�����SsR�J++���b�El��)�˺�;�44�U���j�����D)~Y +��P� �O�L�*����vή��lr�1��t���Fk<ݲ���Am�`@9��*r�U�qó��ƓW�\?׏F��������JU�
��������J��bNȂ��b��ik�Uيǣ�h8����-��b�%�"Jh��.0\v�EhY�F��.qD���[d.��/�_��;t�sk���w�;�\�.��ҦkmAkc���5N�F��_~P�
F�o	�t�a��m�a�_T�S��K�^���xi���vm�h��K�z&7���K�e�j�y&�P�%˳�������o��sKRNm���� [�����hQN���D,~�X�e���Uc��OP�����#]��/l�9�,Ȓ��I�+�K��X��e4�Lgrz��^�ؗk�+�z-0��?<��k�u�}yk��m+�Y��Z��|����҅H��I<	�ǋ����*���`�Қ{�7ĒX�$��r8�Yd������W)�¶�$��L�%�&� ���7���v*��\r�vX1��Q�V��m���T/���!4�]NBcSrx�[ux�.�M7./�ճ��g�� hBM��}P��,޸w��<L�� p��'k9�#W�N/��Y+u
�(XơUJ/e�2^>����4�:��w�QQIb�1)���9��"��:r{���;��W�N6E�z�BDA�J�i8�=��x�0���n��y���"DU��,3Y��Ƈ*���a_� J���3}�j�m_z�'�����Ղ�L��g�\�N���8������O�����2(�G��E�Z:R�a�������
���P��f.�:�\XOR��NBv2�w���|��~�iM���Z�-�
�ꋐ����s�s��j���Vה����}�ʻ>���.ދ���nF5��l�H��G�鰀RfD��{Vڃ�r�#Ş�f0�]U��
���$w��/���Eܷ��Z���1�?� �A���Wy)+6#x���1�%���\5^Tj>�y�H��L�^֓ؤ^^��H�||W
~���r���b�j���6�/gK;��^Y�z�Vu2������ʦ�J:��k԰(^�X/g]�P~��2�.H{�B��.c�-a�Z�������
cY+
�6=�B�"�����>=���n��fy8w��zӽ�6����P��_dKRl�����'���R�����^��	��M�i�?t�S�.U���g��Iu&v+
��S ף������4���&[O��CXt�=��N�2F�w�O(��M��+��l_|P{EEN�H��a����5��q0�Z�z7��9ƶ,]lˮ�2��#\�+⋌�h���#D&.|
8uo{|�"©$���M7{�h"�X�3ύ͍)�>ʹ���n��͞�������	��L�^(�9��>f$���%��P|=�Ԡ�?��Cv?�u�j�xc��r��ϓ��n��4]��XLꄥhآ0z�������pYح�z���
�v��9�.x���eٻſ�%+���V�%O���]xX��u�v\Q<��?�HU��x�����Ƒ,?}��"[��a�����&���LR� [��+2/�Ղ݄��)�ag�U'~iBR'{cő�en�">�sX:^��\�.ʣ�m
�G�Ķ�ܙ���}&ŦXy��u�
<�����f؞������x��ɔ��x��IMב��t���4l��pm�#��L\rHV,��`y���Fo8p�IN����o�����M=e��M>k�6��N��~MJ�������l̦q��ޜ	�؅Z��*�$�u�b�ݷh���A!�Ĳ�+�,��k�Hu��(�<zs>݋
nNT�xQ0]�����K��Z�,���,���6K�l�nEŵ�jn�_% �{;�!,݉
�|4�����l8JySX�Qz/i�%Јc<�lװ����e�eWHg�ܰ�T}�j9�n��20c"� �f"T�n9V����f2��M(���Ǳލ���sf|l��b��DE!gV07�3A<���8���u}ڧ�2Ӝ�{=ᱤU�-��|{%��G���	Ӟ�9<i�̌�S�և[a�����]�V8�y���0?uL8\xF�K���k���e&Twv�g��q1�x)�@�N:L�	������	���02DӦ�t�.w�
�J�97�}}Z�8�&������q�Ť�\�<J��*�z���@��ˏ����/��4�NڇyH�U=�@�-�b��V<�)��nRj���=ZwS>v)��K�;�]��je�I��E��#ѧ�Q=�#�1]�lN4���L���R�a4�`!���2"r]t�8Gu*g}�A��&�Vo1�'�
�N��y�[)��g�	;�[оi1�i]��.gyf]BYG�<0=l�����Lz��Kyaڒ'sJ:��
���+�n��t[CWQ�~3	e��C`�jEAw�
��[4&�����|J�dY�[f#��Р9�=��v�����������l�[������r����`�!c\D�O�m��6$�l8E�ɴp�뫄��Q1!��n,Zde�`��(�DZ~CS�'q����dQ�ET������x�Q�r���t��偒z��8��[����/ ��
-�'���_����!M,���D���銁�y#�AEosK��T"�o��S�)�Ȕ��JBiݤ[N�TȁJپY;0LF�rI�cT$�PM�H�@u��;:YjY�)�R���ʈ*�l<jY*�R��m�v���P��✆�굌�ꕬ��s!M����d:h�dr�gJ����\�Bf��������mP�^�B�9:9<>���H�mH�z��3<uH�qR�)�ې�:�陓*���>^ǰF�q<�'W�4KfR�I!ڜf��Q9Y@�מy��*��"����º��;�&�?�v�C@�$�FĬ�C≘gY�7%�6��]��Ti]-1�Z<;��X+�u ����/��h��'zRW�nq0�Z`ި��'!c�A�&�E�,QbM-�5�W�&�����q�����0'��ҹڠX�<#��V�
�*��o���?6����%f궬ǥ�iG���[EI����w|"�r�b�L_3��8���+l�ࢦ���\��l� 1� �yqg�md�pg�����t'"ؕ6ڜ(�P]E�$�2���`� �F<�[��w���m_K9Te��b�� �	  t���H;���H��dѵD�@����	D���.����بW�&�(S�.�k1M>d#��t�R��T��O�DD��PY� ]��`4}W���b���n���t�XwqX��RǕ���j���w�c	dJ���!�#�\�4o�z����z�Y�2ɟ/�
S\v0�y��:`���������c�D<�Ջf!E�P]��`��,���T����n@[���2ٝ��UԎ��zp�Q9�E*˺���z�9�Ѕ�4���m�6⍆Ah��"��[�<��#0�EtGkdxq��ŚZ14(��Bz�IH/'ct&�Z���<T�T9���2ZI���>j r����S��ґԀ�o��QuG1ڢ��J��Ԯz|ƾ���<���9ꓣ|���x����8��[I��VL����C�0���d<���8.���;^..�AǸ�_O���mܟ�i��}Ⱥ����O����;a�Lg�)�mSw�9�� 9�RWS��6�t�]�K ௧��IoWc_Ա"g����	d�7tdȔț?X>��A=U�P�H˚���[�/J^��Q��w�,.:�Uz��X�F=7�d�壨�
���XG���*�Y5+�Fy������J�U�s�#���u_A�xx{����p��+��Q�uV�.)	��v��i(��B��o�����v�1tF����8P�:둹���V��Ƥ����ne����G����ە-�̶uW9��g_�1YŻ)rY̥1~�ƄuMG�9wD�ȳ��&�2gD��Fx��s�d;�)�N5�����[��'���}E������b��FjF�#e"[
�+h���P��0U���kע�%�Žh)9�%G���F�{�@�ԩ,��cY8�æ�"�9.��(��a�1���
��S��q�3$k�G#�a�?�#����ku?^����R���V������9ݦ��T� �R�T�r<�4*U�U!��Cq]�l]w(]���#h]��	�)�C3�`:0���ŕ�_��n�7��w�ŝ��e� �#fy�v93PL7�>��s��t�&*v/��
��^*��H<��Z�pʆw7���|�ի�^)ʚ�����`��oVg*,�Ez=��-��׊����9*�fP�ϋ����ܒ�%����I�%m���x�|y��j0�h��޷{ݭa��毧����j�ĳ���
c�A��dn$p�æ�����|[��"[E{�����tv�R�IVx%BK5���.����F9ڌVQ�����~���X��C'<�8��:�Xk:L-(����I��t܂�D'Jʙ9��p߇O��
�vxΧ�a��C�_z��?��vљ*��,�,�R����I�N5������w's���^R�4h=�Z��Cx73�0'9� ��3��N����,s�) Ӥе��wڻ��<�Ȑ�'= ��C��2�j觐i�h�H��<Qe��쁥t�8���V|6e�������B��I/w>Es1���x�M�B5J,.)tNs���Jej������ǅVՒVeu��e���b�Jl#/S�R�.(�4�X�����ɑ���8*BR�cRr7�\*� �dAA<q&��4<�%�¦��	B��:�y#� p��0� ��IPl�G^�X�s`^%��0;��خ7?�L-�e�+���n�Qs6i����`�E{�QH{�̞�;6Z�/;�כ��q�\�X.���\j��{�&�:#m@�F2�L����(�;��\1�#�4�*�Jg��� �����/`�{����-�,n6d�����?���SZ��4���� ~u���gTh�ª�/y-߁m�Z���uyP�"�
�7�+O�q���X�pa�*7UH!��݁�<��GZW����R۱ĩ������O
M)A�I�R0F�W��Q2Gs�Yx7��{4����f>�z`�G��7m���#�9�˺7������ɭ���,�f�i��7���.6E���������H� �t�(&S�*Ξ�/_ֻ��s<x����NG0�[�ѕ�V~�"'� (��+$��T��t����f�T�,��bvG��	��l�}tv�x�.tlx}�>U��������:��տAi�#*��ET�o����z����P�GiE�Q���5o�nd-�K-`
n�i���B�}�t;��N�����w���z��KC#��Tm���ЯK�oj�~�MPR�7��������Y����$�:�]��~N:fOJ S&J�}��t�D�b��s�.�U�6���N�<R�ڌ��@�rp��0��bf��D[�3�;__\�����@��Z<��p7�&�0i��̘lU%Vu�RM�o������Uw��x�X���Y�w�a[��)��\�X�D��َRQ&�$=����؈bpa�l1�"5��i6���>�%      �      x������ � �      �      x���͖%����ŧ�լ�:�o`�9c�MR�4�ѦD�Ȳ��:��3��Al?��a�� �D2��m���k��G ��	ˍ
�^lr7zQ�E}�觃�nY��ϛ?}u��]������|���o��H��$�A�A��Kqex`h�a�a+è;eW����"���d1�ar3Mp?f��e��WI��PZ�i��Q�p�ή�Ю�'����g�D��.)������BQK�W�S����������B�@�w�ȧ����~�������n�Y�%�2�+� ��K�'j�$�(PO�q5�:.Dt+1����)$�m�?��ܝ����_�����(%�ȨȦԝvz5�b��Ŷ^f�P�W˂'�D4Q'W���̸Y$�^w�ھD6�-~�q�4���~���	��n��(@G@����-��7ػPm����oޔ�=>�tc}��x��w��jw�����������	�5w�����%���}���S^�/M��O��Xg;�}Z�!L6haZDbX�C�'�oRQ��%�:c���J�+1�D0C4�Q�Q߹�z� �#	�p¹:�������E=~�MK�S �� :~!�NǼ�$�'J��Cs?y�dI7��1����r�}��A�(����ӡmv9L��WI�k~��k���.%	�h���[���*�ʣ����.>�Du-q Qd���Ω�% Z���?r�K=��l6u�� ����a֖�7�����|��g�|v��W���qet���~�;[;�x���#;naڊS9b��[��� r8]F�K8��MWߦǷN��.TK���f�E��
�JU�JwJsߡВ���|��<��"�O~��ab�ۮ6.�S��JI8E]�T��������K�7;���X��W��c�:�?{���oon�����
�W��t����<��������s��w�Oo���W� (���v�G�4P��&�4P�V.�$�V��
o����"��i�������KE������������ͯ_�r�t���ool1_�t<�x��ف�pkz	Ow<��`C�F ���3��n6 �p�?�]q���x+D��n��M���+n�4�.��7~
��Kpq�ywag����tagM71����t�"} M�	��Kȕ�� ւ���y�/��_��~u���s�4�5�Ьh��M!;�!���$��B�����Տ�/�J�L� ͋��2p��ϡ}L�k�� ����OIi_Z�E�v]'�Ϯ�u-�k�؝mx�Ÿ&�-q�97�qM!��!n�c ���%�Y!Cܯҝ�6e�d�f�w�d_͎�εn\�Lu�	c[-A�{�C�ֈ-��[�����A��X+A��¡�w��X��Ħ��Uk��ZQ�݇p����Ҷ��Mi;�j��l��w
�xo�_=���-��mVkV[Y��M��I�b�R�o��-�-�uw�_��N�D�<��٭m��c��,���D������o?��Ͼ��7��ٷ�~�//���E�:��wF"Wp�D����Y��{�5��D�M	q]�y'�8{+s8�%�ʫZ��Bi�B���6#h�÷)�M�<;<Nv_�z۳������M���E	2��#|�Kdp�#܎_$� �o�Ė��S40U�A^K��M�lS�C�DQ������d�vi�%��[��>���|��_>�������/?���o�{�=�-C�>4֗^�����ǖ/M�o��$b}��JN�mXD��k���cԇ�2��f������9�|��	9��Y{�`$��9�Pһ8�
mٗj�T]�f��C�u�����b�4��<[�$��W�����p��;���v����ٿ�����~���n?�����.�ﾽ�⳯����͒N��h{2#�W������-\(���L틇��<ܔ@��]�d&�YU͍��`�]l�T�β`2���!�(F�`9�s�>&ɺ��̘��0fŘY���_�R �$�(������-�X������2L\RjW�YU���*K�����wE�=+�!�d�.�cNbXaZ1�͖�е"�ͦE�(:�R�,��f��}��Sv�X.���9!v%#�d�Sq��dEȨ���nC��F�� *a���,��������ZS��.��&�<&��;[�ҋ�=<>�~���(qw�����nI_�}���d��GL=��m�g9���H;RZ�Y����j�,�o)�s�����hGJ�QK6�0Ƃ)�s��h71L,ؑ�z�%�.��<�#Q��!b&ˑ�:�I(�d�'$�-���Tظ	�C"zK�4�]C��&���Jq׼T�}����~�Z�	�q`=l�5�c�E)�-�!g)f1����*}i�¶-`oʈ]Z�K�F{Sf��	������ڱ����R�.�;�7/�e������	��emq��XL� �ß�H�|��7�`���i�zGO�(�&�L�ް��0B����^����_���������ӯ��Hv���Wu)����Ju$a�!'�.��P�w~b��9�+Z�=J�� L(cB6l�=e/Q�<1��(���#ir��G��D��ɐs�p0�I/;���n�Gȧ�I�sH����?g+��dX���ޘK!�k�q5;:�u��6��4�5��x�ܫ���/A�}��n�|�N� Ø0�+g������s�4��ι�)Z�F�V�3r��.D�U�pWb�BBf��!�H�l��u��r��\�����8�u"D�׭���b$���9��Q�lB&�I써�;�H�;�.WƱ�f�ݱ�z���g�	�QxN�sp܊���֜!�Ą1��)!���A�y��D2e��,6�����e�f%����9᧽� ��� �Kr�b�^K�1I|y&�_vg�\QN4*'�m�O�����+�O�o_?ݿ�}��Ǜ��I��pX��#�Ow�S�MJ_-���K_������ŗ/������?��{�R�*[d����%�'9�L�Wڠ�ܾ����6�'|�������������O?=�m���^?�Q������DW˪�,��	�.��:-{z,������;��8���CM��̷#�/o��}�*>�$�n�zZ������P5��"M�$���dJz���V���D�gO�?�z���'8�&;��2�F�p-}���=S���CG�N������{���4�9D��;� �&�Y�H�;���n�ͳ �B�59oe �����7��|���K�༛�7��Y8H�f�a�Tn��t�)d��i:�"�g���R���U	�F��fٯ�C��I���M!��S�,���BD����gM�=�IuݠS���>�����y�N��g�u�PJeڍOs�ۃA◿������_���?>�U�l�I�;O4��"�i}�W�Vb���սE��~|x���?�~������ba�L�����t��z�q`,�
����F1���T�9��n��i�J��r"Z%=�,aI��K|'�PK����o_|���X~Y$�ܵ9Zӑ�eD@����LCeO���:��O&�'=pI�B�?')iOz�"�\<遦�3�-��t;���y��TO?�{s�e��r@���x�����.ta�VzH���,�5J5����8r߶��ѿ'�p��SC8O�@�y�$���m��l�-�֫�	4���'�q��O�"'�=ɋ�	)�'y�j�A���8kj��E��~~���6o~�+c��X�ʋ���� V�/mrDZ���K��4D�QL���sΞT�J�=�z�D�9e���((Qn�(�=���D2�#��u�z�0c���+��͆#;S�QO��ݿ�����w�?<����Hg�}w|��b+	+K{A�ZppP+œ�������S���2���9��9_��I�sĳ,/�$n�XS���K<�.�J�h��oRW���!��J����ol�S���)\7���闇�o�_��I��ߛ�f�ψ��$��*�I�<��
�7Z�����1rw$y�+B������8	�    ��n�z�L����h��nq;k#����Û�lʖ�	��{�M�o�i���Ś1ǆ�HR-P��D8a�9,6S�	�H�1��z��e��J��p�bx�E�P�i���f������[w�̶V�ȓ�:	"k��z	�h?�pC����m�(�b���tLO:�f?+�=���lE���nx�6}�&{X�z�ȵ���_��#�r;�9��Kiщ��)�!ys��V�"Li�r{�*a��*��e>�����<�*)}O��i�=���R2��N�m}�!���+ �CH �Cz��w��O�B�N�i��?�aŀ��ijO�"g���"��\mg��K6��t��¶���ݽu�^�'t�D�Ȓz ��7`���9�Ķ����  �r�����Fm��c���t�fy ��{�&}T�����)�PSZL�ܓ9�$<����|h�=FHQz�v�~ШT��ׯ~������>�?>�������ݺx��Q,g�Iv�C�ㅞ$��-��ɌcH��y( ��I\�C� �qr�-�n7�H[}d�z�%�]<�����8RA�����j�"o�3�D��d��y�u�����'bc����噻��Ie�c����O:�3�m�����K:����Ik<�)�v�'�� 3�(�n7x���j�o7x�琈y�X�:��O��ٶp�<i�g!ܵ�D��xGH�;B������$��K6���:S�اf�����q���5*2^�ID�ņ�x��^�Y�qf#f�ԌW�"�<e(!'��VS3x��&�k�r9-.%	b����絘FX	"G�aQ"D��âE�p�p%.����f�K�?[��c%���i�,]����?�H���5�w�&���rOl3���BU��Z+Q���@��3�w�e
�����@�b�k���>��G<�3�p i1u�������xm��0H\L̀G�|�&��8�����!nPF��!nP�rH�speL���11nP^�y�dvP�t�$�^�HWN��TQ�:u`���>�*I��C��h)o^�7�a��,!A+	2�o̶5�f���ļ�����[b$��� ���ʐ����q�`>��| #M�Y8���/L��a�@:�2l�1!��b�)��^�0������@�c�u�4�9��$�o����w �CUt�j�Q��R+��ڛ �.�yR�R��D�>v^��0��w 91�^���l �o����Lz	$��.	�1 ��� �ZH�C�g���Rp;H=71^�fV�+��7���	$��!;e��F�J���6���\��*U۬6L85k�G�-̗��}x{���7y2������^��vs{)W�۩�� �dg�&=�z_�����^z�Y1p�
�#����\!�����;<�N��P�;�<�d�Ѧ�5��U8���T'	(��M��R��C0�<4Ŧ*��Ɇ�2 TZ�Wb�,Q!vv�¢x ��q�e��G���tV�u,X���&ם(Aƽ��
x �7ο�
�Y�nI�&��G���iF��@�;/U��|�<�f���]�pش��Ӹ����;	3�b����g����6$H�a�����<>I����ðHY��Yl�|����%�ᵦ:w�!CF��šYl� p�f[�m�� '�$x	���y�������m 'l-D	"M!I�G���
���!*"gE�!�{�d�aPc�gy�I�:�� �sd���$ș��Ŗ�)�$�\�1���g�%��n�O����^o@��"�i��@�AU��-�r����d[�c"'��w��2YVT��	S�$��w؛��c��T#�(�iݟ~� �\%吚�Z�E�Pe�G�K{�Ԭ��q�lS�͚�։K3a?���]у�+|���$��]�����
q�n'�j(ĥY��u�q�t��J�Tq\��]r\��׺�4�,�x>`)�\��@�{u���o���Ϡ� ���t�%�L�$������iQ-"�4��.6*2gcH�3Y����ϲGeĖ��DTV��0�D�EE�kִ��L�Nfq��
"exl��$U��R>P�(�[`��E����D�
����=E�L75�Z��+�8Q�!L͑��1t)�,�s�Q[�)�]$����l���n!�����6L�~����7��<��񇇿�<j�^�M�<�P>��U�=:�=��;�+����ÕT䩞b��#Vwv���{��ݛ���|����M(_�l�va�j���Y|���WzfYqp��,<��R*p0��T�׳��(	�I�ը�26e�ؔmx�ٔ1�SE�N��D� K�'�
u�ȉ�u�#��㌨�@�}�q��}�'I���v�~��/�r_ԖjP�;��%P�ː0@���Qc=Z=K�E�� �kY\dd����%{k��c�!_	���iI��C�N�t����7#isM�^(���0�"��D8��-��ز���˱n�E���qa�T2���t�H�!p�ݡ@]����G�i\�F��:8؏�Z�L����2
L�4���ϋf�x���'�cp�ӭ'��x�??��G(�$Q���Q�-��P��ȑR"v��{��-������ ���Z�]�.�<*������U��p��*�$ѵ�[\yHOg���its�`�l#�� �'#�|�(Bė+#its�0��re$�nNIHI<�lI��S5FMZS������l�j6f__���I$�nN44�M{�+3�'/"ixs�]֯'��E$A�^_̈���{�5�;S["��7��//ER��31	�{��X�Q����D�� b%�H��D� I�;�>:��YV���c�$��!
��z���\"�{Qr����y��c��#�b3Y;@Z�!&�ޘ:/������u{�W�a��;�qr��t����r&��`:��:�r��+ !q���mYH�;��7g̘4�9F�)��7g�������4�@�/��g�*k�?vu|X�'��B�p W�%&#�s�pꗑ�#�s�|#-��7��C��D�Y�iW+ry>a��Y�����l:��T([S��!遱�}F�A�k%R��P��"�H��Sd�H��t2�j��@M+�Q�D��"?a�H�;����s���L��@N,x������D-�����֠�ś��>���%5���L��fq�zC�*�e�i�?�8�)�C�M;��8�૑8�M�>2�A"U0�4m�$��h%`@�I��补��f��eT'�V�I�):���&a�����;�UM��p�K�ћ����j�g��% r�=�fx�V"a��I�A�Ur]_%gJ&T Ö�yo=�Z�!��(��A�0c,�ɟ/�Ц@U%p��'���%�Vs� \<����O(@���X����`�1����2�꤃_N��IG	"+�I�!�ѵd"n��Q��n_�e�'�/l	'cĖ`�>�y��k2d�t u��G;χ�8�5d�F�{��R���ZH�K��g2A��4٬ѓ���G�	��+�Im�*��r�p�E���4h�%s6fF
q��hP�/Y-�F�|�#C+
�%7ݱrφ)��q��DE��1M���:	�z��z�;b��dÅ�sX2�K-&�^�Ø,v���p��cv���f592��9d1ŋ��)	�P�G`�#ݹ
��h��[�&�#���XXYaʂ)����3��8��@d�!��[��R�2<Ӥb���9.�@�|#�'$�p��9��\� �5��9�j�E���SOfY��?�T�Z�Ȳ@�d���9ew����%o%����jt�;	3n��%�/�Ҿ]�A�D�ăZt�G�K[���E�|����`ȴ�E��"Cp`L[Uv��RP�/W�.}�ES�0�Å�˕�K�Y��C,�NL��$�x�����m��.�)¥]b�@�"���S $	c1+a��O��\�%v
Dua��)��A�]�7?�� �{���Z/;�h�c��UuL���v�*b�Ѯm=����������<>ݮ<�����Q����0�%� ��� 	    �@�z�sU%�_��&T���K�f�4���@M�8L(
��R�X��df�槇ʃFG�����V�0�ވ����|���7�ˢ$x�g��"��Q<�P�"ZD�T>}��	�([{�O2�0�"LB503:q}��4�}4ZnZ�U�(�xb��lK�����[2�&�1���7'�z�X	"�43�]�ks�%�X�0C�wPE���ʐf��<&�H��fQ���e�� j��,���Ҍ6�)�_���1"D�f�� �ͨ!�M]�X�����?��8�؍�ex�z� ����	�L���$�Qx�]�s오Y'�t�f��D$�@�ID2�1���_4�$~���ëo_>>=ԓ�F�$�9pw���8i�����H�"xM�>)��E�h۠{J�/I2ޜ6$,�4�q�?�|� ����"T
��T���|�$�cS�C6m6t���}�	�i�5����:V�T�23���=�@<6��֡Μf�ۓjāK�
��%zW�2{�(���mwu�d�%��9D�KgH� �k)E��[{f!�o
�+�d��B��R������g��p��[�_�+�Z��Ima�I�3!�-�֢C�֗�����KZ��6�M~,�E��.���
�]�n�)U��l�|kV�{��t�BR��O��r"�%Y��B��a:Ajy��,�	@��i���G�h"�s�!F�lW.(#�6翁d�ϓe�� '�!�j�)��	"��͌(1Nl�]!R'��f�~1����:������I���L�ޕ aiDoS��rPD�vg,��afS����� ��7N��8x�9d�m]9-i$Z�~:��qW]CG�	���qd�n�4�t�"�r�<8��mR�����ߌIF,`��_�1�"�p�jm�����׿<<?���x1R	�4L��k�rXZb�~�+���,x5�϶,�-���H:� h��%���iR[��A��(�K���T}ʴ���_�~�mP*�!�~�k��Jk+(��������w�?<���o��rFF`�P`��"e����3$30�e�;�N`�Ed����0�b�k�m�Ԧݎ�v�Q����C�zw܂s=�H���1t�`xW;C�Ol�V247�'53��jm����m�	�u�&�׈o��>��%H�AlKv�hF�>á�t�0`�1J�q���
qxu�mX��T;n�/h%ܠ��xİ����p#Bz�RG�1�!!13^�YwT���l�;B��uNJ�d��!�#��E��l��*_�	2fd6.�"�!'�ɩ�����j�"����m�,���pn�c��׬��J��.�KT�#{���#���e�vT,^m�x�żܨHn�c���"��-���Ho�Sd�Q��h㺕Xl�m�:��I��F����e�Z��ɍ���7�+%bR�ǄBz�2\�c����ƃ�l�13WɍnYE��{,YOS$7�!�P�����E���Z��3�rl[�K�e�["���sȘz�{u����n�O���$�X���z� C��dהV"dx4�q��l�l�ٓ��1�֗߿�z�U [!I������e �p}q[s�p��������������=��s���(�Px�
�D�:��9F�Γ�+�G�-��M�V��[�q�O��G�XW%�.�D�9|Rg��+R�9~W�+��D��HO�c��]����Cʶ~(ι$���~�j��0F���Dg,����2Z,�θ	#�?�%�?�7�d�9nWL��nx�]�5�@(��mhˎ�Rݚ����ӿ�����7��\�`���fܑŅ[�>Zg��'�TâU=M��OE�u�ǟ_�zxs��!�p0�D4�0ϣ�9�F�U�jp�&U�S3$-����H��S�CY�M��1�4I��Jd� }�F�Q�@�N�����Д��~&�+���q��)�`�Hk�C䝥"��w�Z�u@9��Q�5@ē���9���rɚ)�}�Dm!��.�%�q��;Bl/�����~Y -Y�f��kF�>���%����um����%�c��%J��tg&d�v=qӶkg�i�s�X���H��8�ȇi��LTM�IL�Aw��;3Q=i����B¹SM��Eo���[9~W����2<��%�Pd���Q�,�i������F��譝�mw��-8�JO�a�=͗�\1�s�3♆o�e�(f��/7��*���0�A�W̇i|��lM,����e�Ͳ�y��$�j������,>�T{��*�%��a��+0��#�)���f��4�N,&��!7�q� c톽$�H$���u�B⍮+��?��H(�NO0�EB�2攙����Ⱥ����F�Px �h)�	�)Ʉ�ybo�jP�����fH� y{W糩~���kɄs��׭u}ݚ��k)�sL��	O|2�t3FI��խ�x�֨���^��.�f��F�ך1�z�Srf�a�,��''a�b �O^	f���5C���G�5
[�>x�x�q\/��Q�QX�����Bߝkha�/�jDǩI"�!]�*n�wMhAҤ
Λ�_2�/Ӛ��9@,��!N1��I<ߒ�fF��c]4��
+@�#��9exʏYF4	�0H�eD��Cj@����g���"�j�r�p��p���nk<���k�}�N�v�V%W��+A�G2�I�97gI��6M��AwD�]�xx ϲkO�dW�;3ȾCb~���s^z��a�&�Va���T�Zl�(�j�CX#F��T��nC���.�0鄱?{�4�:e���!c�O��I	�C�ܡ�ܜՓ�7��Q�^��$��N�ҫ&��C.�����'V)���H�җD'�+>�~sĉՅT��v��VR�b'�O`�u�l��l������7�)<ܥ�����F�ۉBje��K4�~��ؒ�X�p�r��$�E�ݚ�$߸_?�_,Ӥ�E�9zI�+�:�ĭa��ƒ�P߹�V_��h���]�v_(�+�OÏI�D���c1p��ջ2�M*�2>7��h���$� �oD"�($��r�ފ&	/�N6X=7�/P�?	�I��L����Xb���$��	���a�X2� 4�w�z���$���M;@���*��	��	��vsB�s���LO�hR��I�-�:/�p[9��w!�n��K5q� 3����_%Տ¶�J�'B��Ø֯B�]��C�c������ļK7�]2��[;9r�M������g3�,9v�X�8p�Y�z͊��H՛C<f<���L���!�<M��D�&��w	d(Ul4�z1�	Dz�(�7�!Z��7ǜ�޼� �mFuվ���L�d�Oaq��w2�&	/u�sZ�O��c%��U���QM�]ҫ���0�k��O>�c4)xlҹ�=s���FO�v�W��������@~|�s��$Mz^�ܶ^�,�����M�^���^3?P4ǡp�<��I՛�.��Q߳��mݏ��㈥��o����E��Au�7�\��v4*{�eCt-�E�������Ѩ� T���n���@=��}�u�(�s4�yG�4�=�k���A�-
�h��閴,��H�˯�9)�$���l�s�6(pps1�x������3�������&�^b�"�nCʂ1�qb������3}�T]Z"o��B�B��.܁�mǐ��dJZl�x}@'#AN$�R3Y?Xm��k��ME��r*Eա��L�G��N�xcC�E>���D�������%H�7�ى���&�/��g���1�W�̢Dȶh Q���w��Ҙ��B��;�� �<�a0�2�i���TxL�x���4f��∦��TN�����Q��x	V3�+l^��,A��]A��}�}]���[�� v>�9���
���Q��cD���$�7JEq�ۜ��T(�+��S���;�2N��*�&�9c�
�,��ӭcq��PơɃF�"(��<�6��'��Q�HfO*nF��cڹ�"��    ˋ �"&��%FE	3=�Η����a��%F/���;b�"��a�� �e�� vh��(6�~d��(N��-��X�b�m����$J�'�(��z�G˦�w\�h�_׭G��Jم�&�	�J"��0:�KU�H�TE��[�����롉�2����xxx�.�ZG�r�)��Se��5��r]�#�Pp�;�����v9�բ��(M���k��G���絾)�|[�7�:L�Ζ(�S��9k��
�+�։1�'
��)c��z��ǭ�1Qb�]\c�O;����af��!���B��02��ak�L�c��p��oGabX�ap��ڱ�)k%FU�}�w��:������X����G�cTK��r���t�E�㵁0���Î�a��/	��&���Mr;��<��Q���5�}���b2FE�84���Oӎ����.1v�O�H�qJ(ca%�nJ� �9�`��`t^$�0#���qAB����g,�C�K'��~��e�љ��K��1��	~�ۮ@.�3��)�Jb(?�c<�`�&�b��n���On�"��}�&��O��0O�]\x}���X�{��ҡҼ�$�ҝ��R��M�4�w}��x���^��Y�7�>H��*�L+mC�N]E�ę���Ib��G�;,�>t�9�Q�6A�}�w�b;�qG3$yM0��ze�3�#�A;7��m����I�z��(X	d�n����*���p}	���:
�B5T�t�J�S��� p�.��$����B�F%1�f<��f&jq<�m�t�A@!�/�E8�t�Ζ��NQ�;`���e�8�t�n��e�m4�����.��.q�sq�|�ㄉ%�����ޔ�C�<�I�����0�PzSk�;�3^5-����WA��a��f����c���:��)�,}ÀC"�x����vİac�L^����f��*mJuY�~@�گ��
��)���둶�U�M��$�k�ZT�R�̳]	��� H%"�y$�j�?h�҈H��G@���k��̚M��	���$�<����%�vBTf� 26[{к�3Kh&߉���bz��ޕ-v������@Àw�ivm�2��K�w@����]�����:��ţ�}>�u�(��\<��(m3Ds�$���%�l��)3�r������vy���Em�z�?�cQ�Sڅ-Z/�Q"sV����)ӭ%tJ�~�%6�����{�_���w���w��~�����������7����/Jɢ�����!N�0<�TT��x�&���%keQ+T�p{M��5yh$0�Q.T��ցx�=qpJâj���{���ғ�4,j�,5DB�C%���CV�e�v��[g���Y�-��]�������;�ŚE�]0f�想{�)Y���<23ӌ�����^�uZS����t���5�jLmw5�����p~g8�jM3�n
�{�f��?���vSJO|T_l:�mR�sZ�M�h�o��E���y�}��c+�{���VI�@��k�U�	CL�Zk$�6sĤZ��r;��Z'2�T��^b��VkɎ��1��I�6��퇱�׆���Ib��.����/�OB��=C��OU(�.�5������=oM���������BM�MU��A����a��-���O޳�W�V�9W�V���rM��^��}��}��7@1��S��[�'�A�L�ں���Vnn[���9��u�¢�>�����w׭��	&�ٵ�~����_�z�����Y�G�_\�"M��}��*	 ��gkA��kŘ2
��QA�R1���-��/�HF����T+�ժYE��޿zU�۫��9"�wؽ�i��BѾ�Z��S�W$��jooQ_|��7��|�Yޫ���A��Ѯ�q魰CMj:��r?����g�o��x'#'OasH��ޟh%ƎR���H��i��Z	K����-�.�<XĊE�t�B��x&;_�0�a�Э-��o-�m���Y���MHXw�#�8�h֤TCh�#ݺQÃ�?=<?�ߘ�y
8ib��㐴ˡ�㬽$���!���9^S��|�3;^{��Bϳ{^	&�	e$^�yn��ES�d}�	<�!9`R�Z[SYD�֮���Ņ6�A�OJ��b��-N�q
$o]7X��˷>�c�e����A��ц�-K���X�Ƥ{|�if�(Z��	��&P��RF7�\�J���c^��m��1(+�	���/��E�4�seS�����˛�����]�WR,��!H����z�lR��D������| P%�����\6����u����ls"�5���-xuԚ�B�6+�e(D>��AB�NY�ˮ_,b꓃�:����*�]'cV����{nuփ�$svu�9qc!i�%��6GC}b�뀌V�S
�eo�+Ue���.�of�7���������8��iW�R%�qv�3{\�<�n���,����~�s�O68��ŋ:7���.�l��"����j������$�l;'�,��O7m3%43�R7pR�6B�ۆ���6�A�g]�ۜ���6�A����!�i�f*0��\d�����B����|��m&3�m�O�%��<`漽dV��4`���d��f03�]�@�f0+�Se ci����w_�a���X8�����V����r�H����׼>��4��L��S�Z�J;�L�ӥD�XA���y�-��l��T
�5���� 
 ����k�Y��@KZ2̐�����yH`܁ُ�c�"�c�#�����0NUl�K����$3�pp�o|������y�5�/Bg� ��&2�`�������X32�� ��.�[huכ�:b#�A�nцmX����NI��:V�W��EΛn�"����xKa/�m
��t�b�u�1�Z�7����9t�d(����7�$�8�d��L�W���{��]��{ʪ�qE����>���c	 �G��.�ґ�
l(E��+���C�LW�{B)5�-K����1'�����i�L��]ޓ56�K�Ŗ=����K���&��FSM��C��h����!bxMf4�E��`��Eq&��h�*���k��Y6J�t�YR�|����j�,_�;j�b��s,9
u���kKIX;�t��.�J�p����9xG#+��[(�]O�̎�l'��'0�]ۭq�X��fl�i��Z�TZ�tP(03��s&(��<V,����� 5Ѩ�oU@��f�p~��(��;�mƢ��^M���<-��3���P;�2�1����T,	��6���d�*�u�k�J��<*��/ٿ^EU���?�AT(�v6�3f{	Ĳ�mu�C��~N)��C��LBe��?}��O����iᵘd�?�������Ҋ����@����������hT����5��s�B�W��7:��4��ъ�W��eʒH�H,G�
�4p�jɾ7A�B��2˙V���M7D]��,f"KMWX���.�:<U3R�\���R�ˈ�VzD(=���F���֓	yQ8�w)��ߗo����W�-�{�}�(P������\��`�{s�p3ǡޕ��#���u���W$�
��
�
�o�_��'�Ѝ����+���X�\a�e���
K-��/W�j��^k͓�������zC��?�R2�p�z�eB���?wa�!r�O���VV�|��1��x�N�
�����.P5X�����/^�=�|��(�xe�R������S����N��̼�>a�*o^1U���U���ʎKL��	KV�N�v\��>a�&�	F�O�_����䠹/_��>a˒��',Y���K^S��b�o�=�?t�w{~��S�0�O���"Rh������0J�ϖ�(`)F�m�����mc$x�j���/	F9�"��1�(��$���M��E�C-Z����m�ܢ͋_{N��&H��Bh
���m���
-�R�EѢ5�b��ӎSg���t}
n�nk��9e�[ѪU�@/N�Sf��������t������ß{�^���p_�}����c���!��{���Sd'��m k������L��<�޻5"��|�\A(��S������5   6
rZ��e���h
lӉ�)s���+l��G'Z)��m����q��щ�*�J��N�X�f�Y��~щVk�qU�8��^ы��4F��EW��E���o���SOPk1tU�R*\-����q��r&�O��4�1���#�VyrUI�q�3�vЋb����:F�K��Q�I�u�dw��3�E$����O�K�e;9~OvD;�����N��� Z�ƫ�ڱ���Ղh�%~��+��pl���V��m�@��|��sA��md�z� Z�����J�,f�}�j�Gb��� ����F���a�G��6����ԑה�(8�2<�����%����N"+��1H��O��9�2_c�hެu�ٚ�KKi�y�%]a�u��+,���t���y�D+5u�5lUfj*����t
U�tx�Z$x|�����=��X_��V��)���B����M�1��GJ2���Y���r��[b�����Q��!��8îqŧ��"'��&�;����r�ng��6�-,'�Wإ���
�{XNX���������7�1,'�W�E�Ku�~O�4A��`�c�NX���GG-��bW��+�n��*��C����3|%�Ė`!�����%J�qR�-�]�SA�x|��5�C�(�
3�n��B%�_ސZo�Q�B/)��JC}���J�X�l�G��r�Ş%t��cBҢ-w���O��%�r�d�Q�-��enkَ�䥃.v<�������B�.��j����ϴ�����k�Q"�`���������1׵���2��E�%%2N����ʅ=]V=��'H�HqB�5'lVSC��D���U�[�!s�zz�ĞD��Ҟ�a�꜆���Ȟ�b�Lm�k���Ȟ�ea��	Kv�U�0���	kv����e)������	G��T:��6��ߗo��o���k�]l��[�,1XY^�߻�S� �
���k�5���P����c�,8�5�y���*�35�g`�N�N]�x[~L����J�Wt��
����h��I�'z�Z5	_�W��G�W�l���
����_a��z�f%/��^��O�F�N�x�����w����9||��/����?>S	}��@Q�Մ�Jl&������,�F"�E��>0X��w2T��Mϭ� ڦI�3g����h�t��?C_�W�T+ܕ(�~X[�5�@~z��mqؖy�+�V�t���kM�bQ�\��ڭ��P�dQ�]�8�֛�b�Ӹ��{�h�!�׉����!���p�z��c��$��R�ԫ��v�����X�A۩���9�Q�M���t�RU��ٙS�[:a�|�m��Nح�s4�=GS=e��z��L'�Wӕ	��D���*�~2��a<�d�3N�OB1�k�^ޗ��%ค�z}����OJtgaU=-�9�ũq1"�!>oY�L\�H�x��uO'Q���-�&.^����Ϙos.P�����o�qD)�}N�	�K�8�Ik��V�LT�ԫ�Y]f@6%�%�G���ձ��k���<LT'l�8�X<LT��ۇ�M�2$q��W�{g1�f�1)m�*��ݲ��`e�(�yq�py������m�[��*[=B�_	!�U��/�����=����@�������l��O(�N_a�u�Ѣ�
Y����n�-��[�־�~F?Qt�
v��U�bX�*���s��sĨ�R���2��]��(�\ה2S��!�1��mM�d�Z��1�EӜ0�XB�)�Ls�h�����<�v���.���c��iOدrGC\WN{�;��� �	>�/iO���1�'�X���t��G�^�      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �   �  x���M�� ���)f?j�⟜e$�b�A���s��iL"5��a��s�W�����N�r�mlB���g�#�> >�����ٙ�#
H�E�L�	7f]��E#EI."��F7U�V��U�Y�����q��`G�:u��*FQ�9��Đ'&�jsY����`z}�zwInTq���㍙g8��[��5��r��z�ѓm�&Z�U&��6�b��m]�����G�;��*Le,�T��L[c:�h�p�H�>c@D_A��h��K��D!���1P0�3��l�sI�:�,O &��Ϥ�����B1�1�X��r�7�����\g�#F6�hc4}5A��ӲB@QV�:p]H�%�
L����L��B�;P�����{$�(/��B���.����/a�{%U�P��Uާo�S�Ҳ���`o6l�Y����x�������`��׀��-A��1j��z^�A��e�מN��Æ:      �      x������ � �      �      x������ � �      �      x������ � �     